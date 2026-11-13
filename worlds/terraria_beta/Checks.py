import dataclasses
import rule_builder.rules
from BaseClasses import Item, Location, CollectionState
from typing import Tuple, Union, Set, List, Dict, override, TYPE_CHECKING

from rule_builder.options import OptionFilter
if TYPE_CHECKING:
    from worlds.terraria_beta import TerrariaWorld
from .Flags import rule_flags, list_flags, tuple_list_flags, is_location_is_item, store_location_name
import string
import pkgutil
from rule_builder.rules import TWorld, Rule, True_, False_, Has, And, Or, HasFromList, HasAny, HasAll, Filtered
from .Options import HealthLogicHandicap, RandomizeNPCs, RandomizeDepth, Mods, RareAchievements, TimeAchievements, \
    HealthLogic, Getfixedboi, FishingSkips, ShimmerSkips

game_name = "Terraria Beta"

class TerrariaItem(Item):
    game = "Terraria"


class TerrariaLocation(Location):
    game = "Terraria"


def add_token(
        tokens: List[Tuple[int, int, Union[str, int, None]]],
        token: Union[str, int],
        token_index: int,
):
    if token == "":
        return
    if type(token) == str:
        tokens.append((token_index, 0, token.rstrip()))
    elif type(token) == int:
        tokens.append((token_index, 1, token))


IDENT = 0
NUM = 1
SEMI = 2
HASH = 3
AT = 4
NOT = 5
AND = 6
OR = 7
LPAREN = 8
RPAREN = 9
END_OF_LINE = 10

CHAR_TO_TOKEN_ID = {
    ";": SEMI,
    "#": HASH,
    "@": AT,
    "~": NOT,
    "&": AND,
    "|": OR,
    "(": LPAREN,
    ")": RPAREN,
}

TOKEN_ID_TO_CHAR = {id: char for char, id in CHAR_TO_TOKEN_ID.items()}


def tokens(rule: str) -> List[Tuple[int, int, Union[str, int, None]]]:
    token_list = []
    token = ""
    token_index = 0
    escaped = False
    for index, char in enumerate(rule):
        if escaped:
            if token == "":
                token_index = index
            token += char
            escaped = False
        elif char == "\\":
            if type(token) == int:
                add_token(token_list, token, token_index)
                token = ""
            escaped = True
        elif char == "/" and token.endswith("/"):
            add_token(token_list, token[:-1], token_index)
            return token_list
        elif token == "" and char.isspace():
            pass
        elif token == "" and char.isdigit():
            token_index = index
            token = int(char)
        elif type(token) == int and char.isdigit():
            token = token * 10 + int(char)
        elif (id := CHAR_TO_TOKEN_ID.get(char)) != None:
            add_token(token_list, token, token_index)
            token_list.append((index, id, None))
            token = ""
        else:
            if token == "":
                token_index = index
            token += char

    add_token(token_list, token, token_index)
    return token_list


NAME = 0
NAME_SEMI = 1
FLAG_OR_SEMI = 2
POST_FLAG = 3
FLAG = 4
FLAG_ARG = 5
FLAG_ARG_END = 6
COND_OR_SEMI = 7
POST_COND = 8
COND = 9
LOC = 10
FN = 11
POST_FN = 12
FN_ARG = 13
FN_ARG_END = 14
END = 15
GOAL = 16

POS_FMT = [
    "name or `#`",
    "`;`",
    "flag or `;`",
    "`;`, `|`, or `(`",
    "flag",
    "text or number",
    "`)`",
    "name, `#`, `@`, `~`, `(`, or `;`",
    "`;`, `&`, `|`, or `)`",
    "name, `#`, `@`, `~`, or `(`",
    "name",
    "name",
    "`(`, `;`, `&`, `|`, or `)`",
    "text or number",
    "`)`",
    "end of line",
    "goal",
]

RWD_NAME = 0
RWD_NAME_SEMI = 1
RWD_FLAG = 2
RWD_FLAG_SEMI = 3
RWD_END = 4
RWD_LABEL = 5

RWD_POS_FMT = ["name or `#`", "`;`", "flag", "`;`", "end of line", "name"]


def unexpected(line: int, char: int, id: int, token, pos, pos_fmt, file):
    if id == IDENT or id == NUM:
        token_fmt = f"`{token}`"
    elif id == END_OF_LINE:
        token_fmt = "end of line"
    else:
        token_fmt = f"`{TOKEN_ID_TO_CHAR[id]}`"

    raise Exception(
        f"in `{file}`, found {token_fmt} at {line + 1}:{char + 1}; expected {pos_fmt[pos]}"
    )


COND_ITEM = 0
COND_LOC = 1
COND_FN = 2
COND_GROUP = 3

OUT_OF_LOGIC = "UT Logic"


class Condition:
    def __init__(
            self,
            # True = positive, False = negative
            sign: bool,
            # See the `COND_*` constants
            type: int,
            # Condition name or list
            condition: Union[str, Tuple[Union[bool, None], List["Condition"]]],
            argument: Union[str, int, None],
    ):
        self.sign = sign
        self.type = type
        self.condition = condition
        self.argument = argument

    def __str__(self):
        prefix = "NOT " if not self.sign else ""
        if type(self.condition) is str:
            return prefix + str(self.condition)
        operator, cond_group = self.condition
        if operator:
            prefix += "ANY "
        elif operator is not None:
            prefix += "ALL "
        return prefix + str(cond_group)

    __repr__ = __str__


class Entry:
    def __init__(
            self,
            name: str,
            # Name to arg
            flags: Dict[str, Union[str, int, None]],
            rule: rule_builder.rules.Rule
    ):
        self.name = name
        self.flags = flags
        self.rule = rule

    def __str__(self):
        return self.name

    __repr__ = __str__


@dataclasses.dataclass()
class HasValid(Rule["TerrariaWorld"], game=game_name):

    item: str

    def _instantiate(self, world: "TerrariaWorld") -> "Resolved":
        if self.item in world.bad_events:
            return False_().resolve(world)
        else:
            return Has(self.item).resolve(world)


@dataclasses.dataclass()
class HasMinion(Rule["TerrariaWorld"], game=game_name):

    target: int

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(self.target, player=world.player, caching_enabled=True)

    class Resolved(Rule.Resolved):
        target: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            count = 1
            for armor, minion in flag_to_items["Armor Minions"]:
                if state.has(armor, self.player):
                    count += minion
                    break
            if count >= self.target:
                return True
            for accessory, minion in flag_to_items["Minions"]:
                if state.has(accessory, self.player):
                    count += minion
                    if count >= self.target:
                        return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            item_dict = {}
            for item in flag_to_items["Armor Minions"] + flag_to_items["Minions"]:
                item_dict[item[0]] = {id(self)}
            return item_dict

def validate_conditions(
        rule: str,
        entry_indices: dict,
        conditions: List[Condition],
):
    for condition in conditions:
        if condition.type == COND_ITEM:
            if condition.condition not in entry_indices:
                raise Exception(
                    f"item `{condition.condition}` in `{rule}` is not defined"
                )
        elif condition.type == COND_LOC:
            if condition.condition not in entry_indices:
                raise Exception(
                    f"location `{condition.condition}` in `{rule}` is not defined"
                )
        elif condition.type == COND_FN:
            if condition.condition not in {
                "npc",
                "npc_rando",
                "depth",
                "depth_unsafe",
                "calamity",
                "fargo",
                "rare",
                "time",
                "pickaxe",
                "hammer",
                "mech_boss",
                "minions",
                "getfixedboi",
                "fishing",
                "shimmer_skips",
                "health",
            }:
                raise Exception(
                    f"function `{condition.condition}` in `{rule}` is not defined"
                )
        elif condition.type == COND_GROUP:
            _, conditions = condition.condition
            validate_conditions(rule, entry_indices, conditions)


def read_data() -> Tuple[
    # Goal to entry index that ends that goal's range and the locations required
    List[Tuple[int, Set[str]]],
    # Entries
    List[Entry],
    # Entry to entry index
    Dict[str, int],
    # Label to rewards
    Dict[str, List[str]],
    # Reward to flags
    Dict[str, Set[str]],
    # Item name to ID
    Dict[str, int],
    # Location name to ID
    Dict[str, int],
    # Location name to Item name
    Dict[str, str],
    # Flag to items
    Dict[str, set]
]:
    next_id = 0x7E0000
    item_name_to_id = {}

    goals = []
    goal_indices = {}
    entry_parts = []
    entries = []
    entry_indices = {}
    loc_to_item = {}
    mech_boss_loc = []
    mech_bosses = []
    final_boss_loc = []
    final_bosses = []

    flag_to_items = {}

    progression = set()

    for line, rule in enumerate(
            pkgutil.get_data(__name__, "Rules.dsv").decode().splitlines()
    ):
        goal = None
        name = None
        flags = {}

        sign = True
        operator = None
        outer = []
        conditions = []

        pos = NAME
        for char, id, token in tokens(rule):
            if pos == NAME:
                if id == IDENT:
                    name = token
                    pos = NAME_SEMI
                elif id == HASH:
                    pos = GOAL
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == NAME_SEMI:
                if id == SEMI:
                    pos = FLAG_OR_SEMI
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG_OR_SEMI:
                if id == IDENT:
                    flag = token
                    pos = POST_FLAG
                elif id == SEMI:
                    pos = COND_OR_SEMI
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == POST_FLAG:
                if id == SEMI:
                    if flag is not None:
                        if flag in flags:
                            raise Exception(
                                f"set flag `{flag}` at {line + 1}:{char + 1} that was already set"
                            )
                        flags[flag] = None
                        flag = None
                    pos = COND_OR_SEMI
                elif id == OR:
                    pos = FLAG
                elif id == LPAREN:
                    pos = FLAG_ARG
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG:
                if id == IDENT:
                    if flag is not None:
                        if flag in flags:
                            raise Exception(
                                f"set flag `{flag}` at {line + 1}:{char + 1} that was already set"
                            )
                        flags[flag] = None
                        flag = None
                    flag = token
                    pos = POST_FLAG
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG_ARG:
                if id == IDENT or id == NUM:
                    if flag in flags:
                        raise Exception(
                            f"set flag `{flag}` at {line + 1}:{char + 1} that was already set"
                        )
                    flags[flag] = token
                    flag = None
                    pos = FLAG_ARG_END
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FLAG_ARG_END:
                if id == RPAREN:
                    pos = POST_FLAG
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == COND_OR_SEMI:
                if id == IDENT:
                    conditions.append(Condition(sign, COND_ITEM, token, None))
                    sign = True
                    pos = POST_COND
                elif id == HASH:
                    pos = LOC
                elif id == AT:
                    pos = FN
                elif id == NOT:
                    sign = not sign
                    pos = COND
                elif id == LPAREN:
                    outer.append((sign, None, conditions))
                    conditions = []
                    sign = True
                    pos = COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == POST_COND:
                if id == SEMI:
                    if outer:
                        raise Exception(
                            f"found `;` at {line + 1}:{char + 1} after unclosed `(`"
                        )
                    pos = END
                elif id == AND:
                    if operator is True:
                        raise Exception(
                            f"found `&` at {line + 1}:{char + 1} in group containing `|`"
                        )
                    operator = False
                    pos = COND
                elif id == OR:
                    if operator is False:
                        raise Exception(
                            f"found `|` at {line + 1}:{char + 1} in group containing `&`"
                        )
                    operator = True
                    pos = COND
                elif id == RPAREN:
                    if not outer:
                        raise Exception(
                            f"found `)` at {line + 1}:{char + 1} without matching `(`"
                        )
                    condition = operator, conditions
                    sign, operator, conditions = outer.pop()
                    conditions.append(Condition(sign, COND_GROUP, condition, None))
                    sign = True
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == COND:
                if id == IDENT:
                    conditions.append(Condition(sign, COND_ITEM, token, None))
                    sign = True
                    pos = POST_COND
                elif id == HASH:
                    pos = LOC
                elif id == AT:
                    pos = FN
                elif id == NOT:
                    sign = not sign
                elif id == LPAREN:
                    outer.append((sign, operator, conditions))
                    conditions = []
                    sign = True
                    operator = None
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == LOC:
                if id == IDENT:
                    conditions.append(Condition(sign, COND_LOC, token, None))
                    sign = True
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FN:
                if id == IDENT:
                    function = token
                    pos = POST_FN
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == POST_FN:
                if id == LPAREN:
                    pos = FN_ARG
                elif id == SEMI:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    pos = END
                elif id == AND:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    sign = True
                    if operator is True:
                        raise Exception(
                            f"found `&` at {line + 1}:{char + 1} in group containing `|`"
                        )
                    operator = False
                    pos = COND
                elif id == OR:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    sign = True
                    if operator is False:
                        raise Exception(
                            f"found `|` at {line + 1}:{char + 1} in group containing `&`"
                        )
                    operator = True
                    pos = COND
                elif id == RPAREN:
                    conditions.append(Condition(sign, COND_FN, function, None))
                    if not outer:
                        raise Exception(
                            f"found `)` at {line + 1}:{char + 1} without matching `(`"
                        )
                    condition = operator, conditions
                    sign, operator, conditions = outer.pop()
                    conditions.append(Condition(sign, COND_GROUP, condition, None))
                    sign = True
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FN_ARG:
                if id == IDENT or id == NUM:
                    conditions.append(Condition(sign, COND_FN, function, token))
                    sign = True
                    pos = FN_ARG_END
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == FN_ARG_END:
                if id == RPAREN:
                    pos = POST_COND
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")
            elif pos == END:
                unexpected(line, char, id, token, pos)
            elif pos == GOAL:
                if id == IDENT:
                    goal = token
                    pos = END
                else:
                    unexpected(line, char, id, token, pos, POS_FMT, "Rules.dsv")

        if pos != NAME and pos != FLAG_OR_SEMI and pos != COND_OR_SEMI and pos != END:
            unexpected(line, char + 1, END_OF_LINE, None, pos, POS_FMT, "Rules.dsv")

        if name:
            if name in entry_indices:
                raise Exception(
                    f"rule `{name}` on line `{line + 1}` shadows a previous rule"
                )
            entry_indices[name] = len(entry_parts)
            entry_parts.append((name, flags, operator, conditions))

            for flag in flags:
                if flag not in rule_flags:
                    raise Exception(
                        f"rule `{name}` on line `{line + 1}` has unrecognized flag `{flag}`"
                    )

            _, is_item = is_location_is_item(list(flags.keys()))
            item_name = name
            if is_item:
                if "Item" in flags:
                    item_name = flags["Item"] or f"Post-{name}"
                if item_name in item_name_to_id:
                    raise Exception(
                        f"item `{item_name}` on line `{line + 1}` shadows a previous item"
                    )
                item_name_to_id[item_name] = next_id
                next_id += 1

            loc_to_item[name] = item_name

            for flag in flags:

                if flag in list_flags:
                    if not flag_to_items.get(flag):
                        flag_to_items[flag] = []
                    if flag in store_location_name:
                        flag_to_items[flag].append(name)
                    else:
                        flag_to_items[flag].append(item_name)

                elif flag in tuple_list_flags:
                    if not flag_to_items.get(flag):
                        flag_to_items[flag] = []
                    if (value := flags.get(flag)) is None:
                        raise Exception(
                            f"item `{name} on line `{line + 1}` has flag {flag} without assigned value"
                        )
                    flag_to_items[flag].append((item_name, value))

            if "Mech Boss" in flags:
                mech_bosses.append(flags["Item"] or f"Post-{name}")
                mech_boss_loc.append(name)

            if "Final Boss" in flags:
                final_bosses.append(flags["Item"] or f"Post-{name}")
                final_boss_loc.append(name)

        if goal:
            if goal in goal_indices:
                raise Exception(
                    f"goal `{goal}` on line `{line + 1}` shadows a previous goal"
                )
            goal_indices[goal] = len(goals)
            goals.append((len(entry_parts), set()))

    def condition_to_rule(cond: Condition) -> Rule:
        if cond.type == COND_ITEM:
            assert isinstance(cond.condition, str)
            cond_name, cond_flags, _, _ = entry_parts[entry_indices[cond.condition]]
            if "Item" in cond_flags:
                cond_name = cond_flags.get("Item") or f"Post-{cond.condition}"
            else:
                cond_name = cond.condition
            assert isinstance(cond_name, str)
            return HasValid(cond_name)
        elif cond.type == COND_LOC:
            _, _, op, conds = entry_parts[entry_indices[cond.condition]]
            return conditions_to_rule(op, conds)
        elif cond.type == COND_FN:
            def option_to_rule(option):
                return True_(options=[OptionFilter(option, cond.sign, "eq")])

            match cond.condition:
                case "npc":
                    assert (isinstance(cond.argument, int))
                    return HasFromList(*(flag_to_items["Npc"] + flag_to_items["Pet"]),
                                       count=cond.argument)
                case "npc_rando":
                    return option_to_rule(RandomizeNPCs)
                case "depth":
                    assert (isinstance(cond.argument, int))
                    return Has("Progressive Depth", count=cond.argument,
                               options=[OptionFilter(RandomizeDepth, 1, "ge")],
                               filtered_resolution=True)
                case "depth_unsafe":
                    assert (isinstance(cond.argument, int) and 0 < cond.argument < 3)
                    return Or(Has(OUT_OF_LOGIC), True_(options=[OptionFilter(RandomizeDepth,
                                                                             RandomizeDepth.option_on + cond.argument,
                                                                             "lt")]))
                case "calamity":
                    return True_(options=[OptionFilter(Mods, "Calamity", "contains")]) if cond.sign else (
                        False_(options=[OptionFilter(Mods, "Calamity", "contains")], filtered_resolution=True)
                    )
                case "fargo":
                    return True_(options=[OptionFilter(Mods, "Fargo", "contains")]) if cond.sign else (
                        False_(options=[OptionFilter(Mods, "Fargo", "contains")], filtered_resolution=True)
                    )
                case "rare":
                    return option_to_rule(RareAchievements)
                case "time":
                    return option_to_rule(TimeAchievements)
                case "pickaxe":
                    if type(cond.argument) is not int:
                        raise Exception("@pickaxe requires an integer argument")

                    eligible_items = []
                    for pickaxe, power in flag_to_items["Pickaxe"]:
                        if power >= cond.argument:
                            eligible_items.append(pickaxe)

                    return HasAny(*eligible_items)
                case "hammer":
                    if type(cond.argument) is not int:
                        raise Exception("@hammer requires an integer argument")

                    eligible_items = []
                    for hammer, power in flag_to_items["Hammer"]:
                        if power >= cond.argument:
                            eligible_items.append(hammer)

                    return HasAny(*eligible_items)
                case "mech_boss":
                    assert (isinstance(cond.argument, int))
                    return HasFromList(*flag_to_items["Mech Boss"], count=cond.argument)
                case "minions":
                    assert (isinstance(cond.argument, int))
                    return HasMinion(cond.argument)
                case "health":
                    if type(cond.argument) is not int:
                        raise Exception("@health requires an integer argument")

                    health_cascade = []

                    # TODO: This probably needs a custom rule
                    def cascade_to_rules():
                        rule_sum = []
                        for h in range(len(health_cascade)):
                            min_handicap = h - len(health_cascade)
                            rule_sum.append(Filtered(health_cascade[h],
                                                     options=[OptionFilter(HealthLogicHandicap,
                                                                           min_handicap,
                                                                           "gt")],
                                                     filtered_resolution=True))
                        return Or(And(*rule_sum, options=[OptionFilter(HealthLogic, 1, "eq")], filtered_resolution=True),
                                  Has(OUT_OF_LOGIC))

                    health_upgrades = flag_to_items["Health"]
                    health_cascade.append(Has(health_upgrades[0]))
                    if cond.argument == 1:
                        return cascade_to_rules()
                    health_cascade.append(HasAll(*health_upgrades[:2]))
                    if cond.argument == 2:
                        return cascade_to_rules()
                    else:
                        for q in range(cond.argument-2):
                            health_cascade.append(HasFromList(
                                *flag_to_items["Quarter Fruit"],
                                count=q+1,
                                options=[OptionFilter(Mods, "Calamity", operator="contains")],
                                filtered_resolution=True
                            ))
                        return cascade_to_rules()
                case "getfixedboi":
                    return option_to_rule(Getfixedboi)
                case "fishing":
                    return option_to_rule(FishingSkips)
                case "shimmer_skips":
                    return option_to_rule(ShimmerSkips)
                case _:
                    raise Exception(f"Unknown function {cond.condition}")
        elif cond.type == COND_GROUP:
            op, conds = cond.condition
            assert (op is not None) and isinstance(conds, list)
            return conditions_to_rule(op, conds)

    def conditions_to_rule(op: Union[str | bool | None], conds: List["Condition"]) -> Rule:
        if op is None:
            if not conds:
                return True_()
            assert len(conds) == 1
            return condition_to_rule(conds[0])
        else:
            assert isinstance(conds, list)
            rule_list = []
            for cond in conds:
                rule_list.append(condition_to_rule(cond) if isinstance(cond.condition, str)
                                 else conditions_to_rule(*cond.condition))
            return Or(*rule_list) if op else And(*rule_list)

    for rule in entries:
        validate_conditions(rule.name, entry_indices, rule.conditions)

    for i in range(len(entry_parts)):
        name, flags, operator, conditions = entry_parts[i]
        assert i == entry_indices[name]
        validate_conditions(name, entry_indices, conditions)
        entries.append(Entry(name, flags, conditions_to_rule(operator, conditions)))

    for rule in entries:
        if "Goal" in rule.flags:
            if (name := rule.flags.get("Goal")) is not None:
                goal_name = name
            else:
                goal_name = (
                    rule.name.translate(str.maketrans("", "", string.punctuation))
                    .replace(" ", "_")
                    .lower()
                )

            _, items = goals[goal_indices[goal_name]]
            items.add(rule.name)

    _, mech_boss_items = goals[goal_indices["mechanical_bosses"]]
    mech_boss_items.update(mech_boss_loc)

    _, final_boss_items = goals[goal_indices["calamity_final_bosses"]]
    final_boss_items.update(final_boss_loc)

    flag_to_items["Armor Minions"] = list(
        sorted(flag_to_items["Armor Minions"], key=lambda item: item[1], reverse=True))

    # Will be randomized via `slot_randoms` / `self.multiworld.random`
    label = None
    labels = {}
    rewards = {}

    for line in pkgutil.get_data(__name__, "Rewards.dsv").decode().splitlines():
        reward = None
        flags = set()

        pos = RWD_NAME
        for char, id, token in tokens(line):
            if pos == RWD_NAME:
                if id == IDENT:
                    reward = f"Reward: {token}"
                    pos = RWD_NAME_SEMI
                elif id == HASH:
                    pos = RWD_LABEL
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_NAME_SEMI:
                if id == SEMI:
                    pos = RWD_FLAG
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_FLAG:
                if id == IDENT:
                    if token in flags:
                        raise Exception(
                            f"set flag `{token}` at {line + 1}:{char + 1} that was already set"
                        )
                    flags.add(token)
                    pos = RWD_FLAG_SEMI
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_FLAG_SEMI:
                if id == SEMI:
                    pos = RWD_END
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_END:
                unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")
            elif pos == RWD_LABEL:
                if id == IDENT:
                    label = token
                    if label in labels:
                        raise Exception(
                            f"started label `{label}` at {line + 1}:{char + 1} that was already used"
                        )
                    labels[label] = []
                    pos = RWD_END
                else:
                    unexpected(line, char, id, token, pos, RWD_POS_FMT, "Rewards.dsv")

        if pos != RWD_NAME and pos != RWD_FLAG and pos != RWD_END:
            unexpected(line, char + 1, END_OF_LINE, None, pos)

        if reward:
            if reward in rewards:
                raise Exception(
                    f"reward `{reward}` on line `{line + 1}` shadows a previous reward"
                )
            rewards[reward] = flags

            if not label:
                raise Exception(
                    f"reward `{reward}` on line `{line + 1}` is not labeled"
                )
            labels[label].append(reward)

            if reward in item_name_to_id:
                raise Exception(
                    f"item `{reward}` on line `{line + 1}` shadows a previous item"
                )
            item_name_to_id[reward] = next_id
            next_id += 1

    item_name_to_id["Reward: Coins"] = next_id
    next_id += 1

    item_name_to_id[OUT_OF_LOGIC] = next_id
    next_id += 1

    location_name_to_id = {}

    for rule in entries:
        is_loc, _ = is_location_is_item(rule.flags)
        if is_loc:
            if rule.name in location_name_to_id:
                raise Exception(f"location `{rule.name}` shadows a previous location")
            location_name_to_id[rule.name] = next_id
            next_id += 1

    return (
        goals,
        entries,
        entry_indices,
        labels,
        rewards,
        item_name_to_id,
        location_name_to_id,
        loc_to_item,
        flag_to_items,
    )


(
    goals,
    entries,
    entry_indices,
    labels,
    rewards,
    item_name_to_id,
    location_name_to_id,
    loc_to_item,
    flag_to_items,
) = read_data()
