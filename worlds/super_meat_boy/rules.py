from BaseClasses import CollectionState, MultiWorld
from typing import Any, Union, Dict, List, TYPE_CHECKING
from .locations import location_table
from .options import SMBOptions
from .regions import connect_regions
from .utils import is_location_enabled
import re

if TYPE_CHECKING:
    from . import SMBWorld

TOKEN_REGEX = re.compile(
    r"""
    (\|.*?\|) |              # Items inside pipes
    (\{.*?\}) |              # Functions inside braces
    (\band\b|\bor\b) |       # Logical operators
    (\() | (\))              # Parentheses
""",
    re.VERBOSE,
)


def tokenize(s: str) -> List[str]:
    """
    Split a requirement string into individual tokens using TOKEN_REGEX.
    Ex. "|item:2| and {func(3)}" into ["|item:2|", "and", "{func(3)}"]
    """
    tokens: List[str] = []
    for match in TOKEN_REGEX.finditer(s):
        token = match.group()
        tokens.append(token.strip())
    return tokens


def parse_item(token: str) -> Dict[str, Union[str, int]]:
    """
    Parse an item or category token.
    Exs:
        "|item:2|" -> {"item": "item", "count": 2}
        "|@category:3|" -> {"category": "category", "count": 3}
    """
    #strip | and @
    val = token[1:-1].strip()

    is_category = val.startswith("@")
    if is_category:
        val = val[1:]

    if ":" in val:
        name, count = val.split(":", 1)
        count = int(count)
    else:
        name = val
        count = 1

    if is_category:
        return {
            "category": name.strip(),
            "count": count,
        }
    else:
        return {
            "item": name.strip(),
            "count": count,
        }


def parse_function(token: str) -> Dict[str, Any]:
    """
    Parse a function token of the form "{func(*args)}"
    """
    val = token[1:-1]  # strip {}
    if "(" in val:
        name, args = val.split("(", 1)
        args = args.rstrip(")")
        args = [eval(arg.strip()) for arg in args.split(",")] if args else []
    else:
        name = val
        args = []
    return {"function": name.strip(), "args": args}


def parse_expression(tokens: List[str]):
    """
    Parse a list of tokens into a nested logical requirement structure
    """

    def parse_tokens(idx: int):
        res = []

        while idx < len(tokens):
            token = tokens[idx]

            if token == "(":
                expr, idx = parse_tokens(idx + 1)
                res.append(expr)
            elif token == ")":
                return combine_logical(res), idx
            elif token in ("and", "or"):
                res.append(token)
            elif token.startswith("|"):
                res.append(parse_item(token))
            elif token.startswith("{"):
                res.append(parse_function(token))
            idx += 1

        return combine_logical(res), idx

    def combine_logical(lst: List[Any]):
        """
        Convert a flat list with and/or into nested dicts.

        Ex: [A, "and", B, "or", C] -> {"or": [{"and": [A, B]}, C]}
        """
        if not lst:
            return {}
        while "and" in lst or "or" in lst:
            for i, val in enumerate(lst):
                if val in ("and", "or"):
                    left = lst[i - 1]
                    right = lst[i + 1]
                    lst[i - 1 : i + 2] = [{val: [left, right]}]
                    break
        return lst[0]

    parsed, _ = parse_tokens(0)
    return parsed


def evaluate_requirement(world: MultiWorld, options: SMBOptions, state: CollectionState, player: int, node: Any) -> bool:
    # No requirement
    if node is None or node == {}:
        return True

    # Logical AND
    if isinstance(node, dict) and "and" in node:
        return all(evaluate_requirement(world, options, state, player, child) for child in node["and"])

    # Logical OR
    if isinstance(node, dict) and "or" in node:
        return any(evaluate_requirement(world, options, state, player, child) for child in node["or"])

    # Item requirement
    if isinstance(node, dict) and "item" in node:
        return state.has(node["item"], player, node.get("count", 1))

    # Category requirement
    if isinstance(node, dict) and "category" in node:
        return state.has_group(node["category"], player, node.get("count", 1))

    # Function requirement
    if isinstance(node, dict) and "function" in node:
        func_name = node["function"]
        args = node.get("args", [])

        func = FUNCTION_TABLE[func_name]
        return func(options, state, player, *args)

    raise TypeError(f"Invalid requirement node: {node}")


def parse_requirement(world: MultiWorld, options: SMBOptions, state: CollectionState, player: int, req: str) -> bool:
    if not req:
        return True

    tokens = tokenize(req)
    parsed = parse_expression(tokens)

    return evaluate_requirement(world, options, state, player, parsed)


def boss_req(options: SMBOptions, state: CollectionState, player: int, chpt: int) -> bool:
    return state.has(f"Chapter {chpt} LW Boss Key", player, options.boss_req.value) and state.has("Meat Boy", player)


def speedrun_req(options: SMBOptions, state: CollectionState, player: int, chpt: int) -> bool:
    return state.has_all([f"{chpt}-{i} A+ Rank" for i in range(1, 21 if chpt != 6 else 6)], player)


def lw_drfetus(options: SMBOptions, state: CollectionState, player: int) -> bool:
    has_boss_keys = state.has("Chapter 6 LW Boss Key", player, options.lw_dr_fetus_req)
    if options.goal == "light_world":
        return state.has_all([f"Chapter {i} Key" for i in range(1, 7)], player) and has_boss_keys

    return has_boss_keys


def dw_drfetus(options: SMBOptions, state: CollectionState, player: int) -> bool:
    has_boss_keys = state.has("DW Dr. Fetus Key", player, options.dw_dr_fetus_req)
    if options.goal == "dark_world":
        return state.has_all([f"Chapter {i} Key" for i in range(1, 7)], player) and has_boss_keys
    
    return has_boss_keys


def prog_character(options: SMBOptions, state: CollectionState, player: int) -> bool:
    return (
        (state.has("Josef", player) and state.has("Bandage", player, 30))
        or (state.has("Naija", player) and state.has("Bandage", player, 50))
        or (state.has("Steve", player) and state.has("Bandage", player, 100))
        or state.has("Commander Video", player)
        or state.has("Jill", player)
        or state.has("Ogmo", player)
        or state.has("Flywrench", player)
        or state.has("The Kid", player)
    )


def bandages(options: SMBOptions, state: CollectionState, player: int, req: int) -> bool:
    counter: int = 0
    if state.has("Chapter 1 Key", player):
        counter += 11
        if options.dark_world.value:
            counter += (
                state.has("1-3 A+ Rank", player)
                + state.has("1-5 A+ Rank", player)
                + state.has("1-10 A+ Rank", player)
                + (state.has("1-13 A+ Rank", player) * 2)
                + state.has("1-14 A+ Rank", player)
                + state.has("1-15 A+ Rank", player)
                + state.has("1-17 A+ Rank", player)
                + state.has("1-19 A+ Rank", player)
            )
    if state.has("Chapter 2 Keys", player):
        counter += 11
        if options.dark_world.value:
            counter += (
                state.has("2-4 A+ Rank", player)
                + (state.has("2-5 A+ Rank", player) * 2)
                + state.has("2-6 A+ Rank", player)
                + state.has("2-7 A+ Rank", player)
                + state.has("2-10 A+ Rank", player)
                + state.has("2-12 A+ Rank", player)
                + state.has("2-15 A+ Rank", player)
                + state.has("2-16 A+ Rank", player)
            )
    if state.has("Chapter 3 Key", player):
        counter += 8
        if options.dark_world.value:
            counter += (
                (state.can_reach_location("3-7WZ Tunnel Vision", player) * 2)
                + state.can_reach_location("3-4 Transmissions (Bandage)", player)
                + state.has("3-3 A+ Rank", player)
                + state.has("3-5 A+ Rank", player)
                + state.has("3-6 A+ Rank", player)
                + state.has("3-7 A+ Rank", player)
                + (state.has("3-8 A+ Rank", player) * 2)
                + state.can_reach_location("3-14X Step One (Bandage)", player)
                + state.has("3-16 A+ Rank", player)
                + state.has("3-19 A+ Rank", player)
            )
    if state.has("Chapter 4 Key", player):
        counter += 11
        if options.dark_world.value:
            counter += (
                state.has("4-3 A+ Rank", player)
                + state.has("4-4 A+ Rank", player)
                + (state.can_reach_location("4-7XWZ MMMMMM", player) * 2)
                + state.has("4-8 A+ Rank", player)
                + state.has("4-10 A+ Rank", player)
                + state.has("4-14 A+ Rank", player)
                + state.has("4-18 A+ Rank", player)
                + state.has("4-19 A+ Rank", player)
            )
    if state.has("Chapter 5 Key", player):
        counter += 11
        if options.dark_world.value:
            counter += (
                state.has("5-4 A+ Rank", player)
                + state.has("5-5 A+ Rank", player)
                + state.has("5-8 A+ Rank", player)
                + state.has("5-10 A+ Rank", player)
                + state.has("5-11 A+ Rank", player)
                + state.has("5-17 A+ Rank", player)
                + state.has("5-18 A+ Rank", player)
                + (state.has("5-20 A+ Rank", player) * 2)
            )

    return counter >= req


FUNCTION_TABLE = {
    "boss_req": lambda options, state, player, chpt: boss_req(options, state, player, chpt),
    "speedrun_req": lambda options, state, player, chpt: speedrun_req(
        options, state, player, chpt
    ),
    "lw_drfetus": lambda options, state, player: lw_drfetus(options, state, player),
    "dw_drfetus": lambda options, state, player: dw_drfetus(options, state, player),
    "prog_character": lambda options, state, player: prog_character(options, state, player),
    "bandages": lambda options, state, player, req: bandages(options, state, player, req),
}


def set_rules(world: MultiWorld, options: SMBOptions, player: int):
    for name, data in location_table.items():
        if not is_location_enabled(options, data):
            continue

        req = data.requirement

        world.get_location(name, player).access_rule = lambda state, req=req: parse_requirement(
            world, options, state, player, req
        )

    connect_regions(world, "Menu", "Initial", player)
    for i in range(1, 6):
        connect_regions(world, "Menu", f"Chapter {i}", player, lambda state, i=i: state.has(f"Chapter {i} Key", player))

    connect_regions(world, "Menu", "Chapter 6", player, lambda state: state.has("Chapter 6 Key", player) and state.has("Meat Boy", player))
    if options.chapter_seven:
        connect_regions(world, "Menu", "Chapter 7", player, lambda state: state.has("Chapter 7 Key", player) and state.has("Bandage Girl", player))

    if options.goal == "light_world_chapter7":
        world.completion_condition[player] = \
            lambda state: state.has("Chapter 7 LW Level Key", player, 20)
    elif options.goal == "dark_world_chapter7":
        world.completion_condition[player] = \
            lambda state: state.has("Chapter 7 DW Level Key", player, 20)
    else:
        world.completion_condition[player] = \
            lambda state: state.has("Victory", player)