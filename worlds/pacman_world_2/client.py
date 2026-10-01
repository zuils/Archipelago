import asyncio
import logging
import struct
from argparse import Namespace
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Type

import Utils
from CommonClient import CommonContext, ClientCommandProcessor, server_loop, gui_enabled, get_base_parser
from NetUtils import ClientStatus, NetworkItem
from .pypine import Pine
from . import locations


logger = logging.getLogger("Client")

# Memory Addresses

GAME_ID: str = "SLUS-20224"

GP: int = 0x5BB070                                # Global Pointer

# Live game state
LEVEL_ID_ADDR: int = 0x49BD2C                     # u32: current level ID
RUNTIME_LEVEL_COMPLETE_ADDR: int = 0x5B7BB0       # u8: runtime level completion flag
FRUIT_ADDR: int = 0x3635E4                        # u32[5]: Cherry, Strawberry, Orange, Apple, Melon
PACDOT_ADDR: int = GP - 0x1120                    # u32: pacDotsEaten (0x5B9F50)
GALAXIAN_ADDR: int = 0x3635F8                     # u32: Galaxian counter

# Saved per-level data: one struct of LEVEL_STEP bytes per level
LEVEL_DATA_BASE: int = 0x49BDC0
LEVEL_STEP: int = 0x88
MAX_LEVEL_ID: int = 48

# Offsets inside a level's saved struct
BEST_TIME_OFFSET: int = 0x04                      # float: best Time Trial time
TOKEN_BASE_OFFSET: int = 0x40                     # first of TOKEN_COUNT token flags
TOKEN_STEP: int = 0x04
TOKEN_COUNT: int = 8
BONUS_TOKEN_1_OFFSET: int = 0x20                  # relative to TOKEN_BASE_OFFSET
BONUS_TOKEN_2_OFFSET: int = 0x24                  # relative to TOKEN_BASE_OFFSET (Time Trial bonus token)

# Time-Trial flags
TT_FLAG_ADDR: int = 0x495C3C
TT_ACTIVE_ADDR: int = 0x5B910C                    # u32: 1 = Time Trial active
TT_TIMER_ADDR: int = 0x5B9114                     # float: Time Trial timer (seconds)
HACK_VALUE: float = 9999.0                        # Best time written during a trial so any run beats it

# Levels with special handling
LEVELS_WITHOUT_TOKENS: Tuple[int, ...] = (4, 8, 12, 16, 20, 24)
TT_BONUS_EXCLUDED_LEVEL: int = 18                 # No Time Trial bonus token here

# Runtime level-complete flag values that count as "completed"
LEVEL_COMPLETE_FLAG_VALUES: Tuple[int, ...] = (1, 0x4B)

# Static data

REGION_NAMES: List[str] = list(dict.fromkeys(data.region for data in locations.location_table.values()))
FINAL_LEVEL_ID: int = len(REGION_NAMES) - 1
FRUIT_NAMES: List[str] = ["Cherry", "Strawberry", "Orange", "Apple", "Melon"]

PINE_ERRORS = (ConnectionError, TimeoutError, Pine.ConnectionError, Pine.DuplicateConnectionError)

# Other stuff

class ConnectionStatus(Enum):
    DISCONNECTED = 0
    GAME_NOT_DETECTED = 1
    CONNECTED = 2


@dataclass
class LevelSnapshot:
    """Everything we poll for the current level, used to diff against the next poll."""
    level_id: int
    fruits: List[int]
    pacdot: int
    galaxian: int
    token_flags: Dict[str, int]
    tt_flag: int


@dataclass(frozen=True)
class LevelGate:
    """How far the player is from being allowed to send checks from a level."""
    levels_missing: int   # Progressive Levels still needed
    tokens_missing: int   # Tokens still needed (final level only)

    @property
    def blocked(self) -> bool:
        return self.levels_missing > 0 or self.tokens_missing > 0


@dataclass
class ActiveTimeTrial:
    """State saved while the Time Trial bonus-token hack is applied."""
    level_id: int
    best_time_address: int
    bonus_token_address: int
    original_best_time: float


# Client

class PacManWorld2CommandProcessor(ClientCommandProcessor):
    pass


class PacManWorld2Context(CommonContext):
    command_processor: Type[PacManWorld2CommandProcessor] = PacManWorld2CommandProcessor
    game: str = "Pac-Man World 2"
    items_handling: int = 0b111

    def __init__(self, server_address: Optional[str] = None, password: Optional[str] = None, slot: int = 28011) -> None:
        super().__init__(server_address, password)

        self.pine: Pine = Pine(slot)
        self.status: ConnectionStatus = ConnectionStatus.DISCONNECTED
        self.game_connected: bool = False
        self.last_status_message: Optional[str] = None

        self.location_name_to_id: Dict[str, int] = {
            name: data.location_id for name, data in locations.location_table.items()
        }

        # Data from the server
        self.slot_data: Dict[str, Any] = {}
        self.progressive_levels: int = 0
        self.tokens_received: int = 0
        self.token_goal: int = 0
        self.goal_location_id: Optional[int] = None
        self.just_connected: bool = False

        # Polling state
        self.prev: Optional[LevelSnapshot] = None
        self.prev_runtime_level_complete: bool = False
        self.time_trial: Optional[ActiveTimeTrial] = None

        # Warning de-duplication
        self.initial_warned_levels: Set[int] = set()
        self.token_warned: bool = False

    # Archipelago server callbacks
    
    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.just_connected = True
            self.token_goal = int(self.slot_data["token_goal"])
            
            goal_location = self.slot_data["goal_location"]
            self.goal_location_id = self.location_name_to_id.get(goal_location)
            logger.info("Connected to Archipelago server.")

        elif cmd == "ReceivedItems":
            if args["index"] == 0:
                self.progressive_levels = 0
                self.tokens_received = 0

            for item_data in args["items"]:
                item = NetworkItem(*item_data)
                self.count_received_item(item)

    def count_received_item(self, item: NetworkItem) -> None:
        item_name = self.item_names.lookup_in_slot(item.item, item.player)
        if item_name == "Progressive Level":
            self.progressive_levels += 1
        elif item_name == "Token":
            self.tokens_received += 1

    async def check_goal(self) -> None:
        if self.finished_game or self.goal_location_id is None:
            return

        if self.goal_location_id in self.checked_locations:
            asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Pac-Man World 2 Client"
        ui.logging_pairs = [("Client", "Archipelago")]
        return ui

    def queue_location(self, region_name: str, location_suffix: str) -> None:
        loc_id = self.location_name_to_id.get(f"{region_name}: {location_suffix}")
        if loc_id is not None and loc_id in self.missing_locations:
            self.locations_checked.add(loc_id)

    # Progression

    def can_access_final_level(self) -> bool:
        return self.progressive_levels >= FINAL_LEVEL_ID and self.tokens_received >= self.token_goal

    def enforce_progression(self) -> None:
        """Used for level locking to prevent the player from playing the next level."""
        unlock_count = min(self.progressive_levels, FINAL_LEVEL_ID)

        for level_id in range(FINAL_LEVEL_ID):
            address = self.get_level_complete_address(level_id)
            if address is None:
                continue

            wanted = 1 if level_id < unlock_count else 0
            if self.pine.read_int32(address) != wanted:
                self.pine.write_int32(address, wanted)

    def get_level_gate(self, level_id: int) -> LevelGate:
        """Level N needs N Progressive Levels, the final level also needs the token goal."""
        levels_missing = max(0, level_id - self.progressive_levels)
        tokens_missing = 0
        if level_id == FINAL_LEVEL_ID:
            tokens_missing = max(0, self.token_goal - self.tokens_received)
        return LevelGate(levels_missing, tokens_missing)

    def warn_blocked(self, level_id: int, gate: LevelGate) -> None:
        if gate.levels_missing:
            logger.warning(
                f"WARNING: Will not send checks out for the level {REGION_NAMES[level_id]}. "
                f"You need {gate.levels_missing} more Progressive Levels."
            )
        if gate.tokens_missing:
            logger.warning(
                f"WARNING: Will not send checks out for tokens. "
                f"You need {gate.tokens_missing} more Tokens to unlock the final level."
            )

    def warn_blocked_once(self, level_id: int, gate: LevelGate) -> None:
        """Entering a locked level warns once per level (and once for the token requirement)."""
        if gate.levels_missing and level_id not in self.initial_warned_levels:
            self.initial_warned_levels.add(level_id)
            logger.warning(
                f"WARNING: Will not send checks out for the level {REGION_NAMES[level_id]}. "
                f"You need {gate.levels_missing} more Progressive Levels."
            )
        if gate.tokens_missing and not self.token_warned:
            self.token_warned = True
            logger.warning(
                f"WARNING: Will not send checks out for tokens. "
                f"You need {gate.tokens_missing} more Tokens to unlock the final level."
            )

    # Address helpers

    @staticmethod
    def get_level_complete_address(level_id: int) -> Optional[int]:
        # MapSelect_CalculateOpens(): *(int *)(&DAT_0049bdc0 + levelID * 0x88)
        if 0 <= level_id <= MAX_LEVEL_ID:
            return LEVEL_DATA_BASE + level_id * LEVEL_STEP
        return None

    def get_level_base(self, level_id: int) -> Optional[int]:
        """Address of the first token flag for a level, or None if it has no tokens."""
        if level_id in LEVELS_WITHOUT_TOKENS:
            return None

        level_complete = self.get_level_complete_address(level_id)
        if level_complete is None:
            return None

        return level_complete + TOKEN_BASE_OFFSET

    def get_token_addresses(self, level_id: int) -> List[Tuple[str, int]]:
        """Return (location suffix, address) for every saved token flag in the level."""
        level_base = self.get_level_base(level_id)
        if level_base is None:
            return []

        addresses = [(f"Token #{i + 1}", level_base + i * TOKEN_STEP) for i in range(TOKEN_COUNT)]
        addresses.append(("Bonus Token #1", level_base + BONUS_TOKEN_1_OFFSET))
        if level_id != 0:
            addresses.append(("Bonus Token #2", level_base + BONUS_TOKEN_2_OFFSET))

        return addresses

    def read_token_flags(self, level_id: int) -> Dict[str, int]:
        return {name: self.pine.read_int32(address) for name, address in self.get_token_addresses(level_id)}

    def get_time_trial_addresses(self, level_id: int) -> Tuple[Optional[int], Optional[int]]:
        """Return (best time address, bonus token address); either may be None if unsupported."""
        if level_id == 0 or level_id in LEVELS_WITHOUT_TOKENS:
            return None, None

        level_complete = self.get_level_complete_address(level_id)
        if level_complete is None:
            return None, None

        best_time_address = level_complete + BEST_TIME_OFFSET
        bonus_token_address = None
        if level_id != TT_BONUS_EXCLUDED_LEVEL:
            bonus_token_address = level_complete + TOKEN_BASE_OFFSET + BONUS_TOKEN_2_OFFSET

        return best_time_address, bonus_token_address

    def get_best_time(self, address: int) -> float:
        return struct.unpack("<f", self.pine.read_bytes(address, 4))[0]

    def set_best_time(self, address: int, value: float) -> None:
        self.pine.write_bytes(address, struct.pack("<f", value))

    # Time Trial hack

    def check_time_trial(self) -> None:
        active = self.pine.read_int32(TT_ACTIVE_ADDR)

        if active == 1 and self.time_trial is None:
            self.start_time_trial()
        elif active == 0 and self.time_trial is not None:
            self.finish_time_trial()

    def start_time_trial(self) -> None:
        level_id = self.pine.read_int32(LEVEL_ID_ADDR)
        if not 0 <= level_id < len(REGION_NAMES):
            return

        best_time_address, bonus_token_address = self.get_time_trial_addresses(level_id)
        if best_time_address is None or bonus_token_address is None:
            return

        self.time_trial = ActiveTimeTrial(
            level_id=level_id,
            best_time_address=best_time_address,
            bonus_token_address=bonus_token_address,
            original_best_time=self.get_best_time(best_time_address),
        )
        self.set_best_time(best_time_address, HACK_VALUE)

        #logger.info(
        #    f"Time trial started: {REGION_NAMES[level_id]} | "
        #    f"Best time: {self.time_trial.original_best_time:.3f}s -> {HACK_VALUE:.3f}s"
        #)

    def finish_time_trial(self) -> None:
        trial = self.time_trial

        current_token = self.pine.read_int32(trial.bonus_token_address)
        if not current_token & 1: # token not awarded
            self.pine.write_int32(trial.bonus_token_address, current_token | 1)

        level_id = (trial.best_time_address - (LEVEL_DATA_BASE + BEST_TIME_OFFSET)) // LEVEL_STEP
        tt_flag_addr = TT_FLAG_ADDR + level_id * LEVEL_STEP
        self.pine.write_int8(tt_flag_addr, 1)

        self.set_best_time(trial.best_time_address, trial.original_best_time)
        self.time_trial = None


    # Location checking

    def check_location(self) -> None:
        if not self.pine.is_connected():
            return

        runtime_level_complete = self.pine.read_int32(RUNTIME_LEVEL_COMPLETE_ADDR) in LEVEL_COMPLETE_FLAG_VALUES
        level_id = self.pine.read_int32(LEVEL_ID_ADDR)

        # TODO: Fix level progression locking mechanism
        # self.enforce_progression()

        # Ignore warp/transition IDs
        if not 0 <= level_id < len(REGION_NAMES):
            return

        gate = self.get_level_gate(level_id)
        if gate.blocked and self.slot_data:
            self.warn_blocked_once(level_id, gate)

        self.check_level_completion(level_id, runtime_level_complete)

        snapshot = self.read_snapshot(level_id)
        self.check_time_trial()

        # First poll after connecting or after changing level
        if self.just_connected:
            self.just_connected = False
            self.prev = snapshot
            return

        if self.prev is None or self.prev.level_id != level_id:
            self.prev = snapshot
            return

        new_checks = self.find_new_checks(self.prev, snapshot)
        self.submit_checks(level_id, gate, new_checks)
        self.prev = snapshot

    def read_snapshot(self, level_id: int) -> LevelSnapshot:
        return LevelSnapshot(
            level_id=level_id,
            fruits=[self.pine.read_int32(FRUIT_ADDR + i * 4) for i in range(len(FRUIT_NAMES))],
            pacdot=self.pine.read_int32(PACDOT_ADDR),
            galaxian=self.pine.read_int32(GALAXIAN_ADDR),
            token_flags=self.read_token_flags(level_id),
            tt_flag=self.pine.read_int32(TT_FLAG_ADDR + level_id * LEVEL_STEP),
        )

    @staticmethod
    def find_new_checks(prev: LevelSnapshot, cur: LevelSnapshot) -> List[str]:
        """Location suffixes for everything gained since the previous poll."""
        checks: List[str] = []

        for fruit_name, before, after in zip(FRUIT_NAMES, prev.fruits, cur.fruits):
            checks += [f"{fruit_name} #{n + 1}" for n in range(before, after)]

        checks += [f"Pac-Dot #{n + 1}" for n in range(prev.pacdot, cur.pacdot)]

        if cur.galaxian > prev.galaxian:
            checks.append("Galaxian")

        for token_name, value in cur.token_flags.items():
            before = prev.token_flags.get(token_name, value)
            if value & 1 and not before & 1:
                checks.append(token_name)

        if cur.tt_flag != 0 and prev.tt_flag == 0:
            checks.append("Time Trial Complete")

        return checks

    def submit_checks(self, level_id: int, gate: LevelGate, checks: List[str]) -> None:
        region_name = REGION_NAMES[level_id]

        for check in checks:
            if gate.blocked:
                self.warn_blocked(level_id, gate)
            else:
                self.queue_location(region_name, check)

    def check_level_completion(self, level_id: int, runtime_level_complete: bool) -> None:
        if runtime_level_complete and not self.prev_runtime_level_complete:
            completed_level_id = self.find_completed_level_id(level_id)
            if completed_level_id is not None:
                self.queue_location(REGION_NAMES[completed_level_id], "Level Complete")

        self.prev_runtime_level_complete = runtime_level_complete

    def find_completed_level_id(self, level_id: int) -> Optional[int]:
        prev_level_id = self.prev.level_id if self.prev else None

        if prev_level_id is not None and prev_level_id != level_id:
            return prev_level_id
        if 0 <= level_id < len(REGION_NAMES):
            return level_id
        return prev_level_id

    # PCSX2 connection

    def connect_game(self) -> ConnectionStatus:
        try:
            if not self.pine.is_connected():
                self.status = ConnectionStatus.DISCONNECTED
                return self.status
            return self.check_game_loaded()
        except PINE_ERRORS:
            self.status = ConnectionStatus.DISCONNECTED
            return self.status

    def check_game_loaded(self) -> ConnectionStatus:
        try:
            game_id = self.pine.get_game_id()
        except PINE_ERRORS:
            self.status = ConnectionStatus.GAME_NOT_DETECTED
            return self.status

        self.status = ConnectionStatus.CONNECTED if game_id == GAME_ID else ConnectionStatus.GAME_NOT_DETECTED
        return self.status

    def disconnect_game(self) -> None:
        self.pine.disconnect()
        self.status = ConnectionStatus.DISCONNECTED

    def poll_game_state(self) -> None:
        """Read the game state in the background. PINE errors are handled by game_watcher."""
        if not self.pine.is_connected():
            self.status = ConnectionStatus.DISCONNECTED
            self.game_connected = False
            return

        if self.check_game_loaded() != ConnectionStatus.CONNECTED:
            self.game_connected = False
            return

        self.status = ConnectionStatus.CONNECTED
        self.game_connected = True
        self.check_location()

    async def game_watcher(self) -> None:
        loop = asyncio.get_running_loop()

        while not self.exit_event.is_set():
            try:
                await loop.run_in_executor(None, self.poll_game_state)
                await self.report_and_send()

            except PINE_ERRORS:
                self.mark_game_disconnected()
                self.report_status("Waiting for PCSX2 to open.")

            except Exception as e:
                logger.debug(f"game_watcher: {e}", exc_info=True)
                self.mark_game_disconnected()
                raise

            await asyncio.sleep(0.1 if self.game_connected else 1.0)

    async def report_and_send(self) -> None:
        if self.game_connected:
            self.report_status(f"Connected to {self.game}.")
            if self.locations_checked:
                await self.check_locations(self.locations_checked)
            await self.check_goal()
        elif self.status == ConnectionStatus.DISCONNECTED:
            self.report_status("Waiting for PCSX2 to open.")
        else:
            self.report_status(f"Connected to PCSX2 - waiting for {self.game} to be loaded.")

    def mark_game_disconnected(self) -> None:
        self.status = ConnectionStatus.DISCONNECTED
        self.game_connected = False

    def report_status(self, message: str) -> None:
        if message != self.last_status_message:
            logger.info(message)
            self.last_status_message = message

    async def on_shutdown(self) -> None:
        if self.time_trial is not None:
            try:
                self.set_best_time(self.time_trial.best_time_address, self.time_trial.original_best_time)
            except Exception:
                pass

        self.disconnect_game()
        super().on_shutdown()

# Main client shenanigans

async def main(args: Namespace) -> None:
    ctx = PacManWorld2Context(args.connect, args.password)

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()

    ctx.run_cli()

    watcher_task = asyncio.create_task(ctx.game_watcher(), name="GameWatcher")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await watcher_task
    await ctx.shutdown()


def launch(*launch_args: str) -> None:
    Utils.init_logging("Pac-Man World 2 Client")

    import colorama

    parser = get_base_parser()
    args: Namespace = parser.parse_args(launch_args)

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == "__main__":
    launch()