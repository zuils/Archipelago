import re
from typing import Any, Union, Dict, List, Tuple, TYPE_CHECKING
from rule_builder.rules import AtLeast, CanReachLocation, Has, HasAll, HasGroup, Rule, True_
from .locations import location_table
from .options import SMBOptions
from .regions import connect_regions
from .utils import is_location_enabled

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


def parse_expression(tokens: List[str]) -> Dict[str, Any]:
    """
    Parse a list of tokens into a nested logical requirement structure
    """

    def parse_tokens(idx: int) -> Tuple[Dict[str, Any], int]:
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

    def combine_logical(lst: List[Any]) -> Dict[str, Any]:
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


def evaluate_requirement(node: Any, options: SMBOptions) -> Rule:
    if node is None or node == {}:
        return True_()

    if isinstance(node, dict) and "and" in node:
        children = iter(node["and"])
        rule = evaluate_requirement(next(children), options)
        for child in children:
            rule = rule & evaluate_requirement(child, options)
        return rule

    if isinstance(node, dict) and "or" in node:
        children = iter(node["or"])
        rule = evaluate_requirement(next(children), options)
        for child in children:
            rule = rule | evaluate_requirement(child, options)
        return rule

    if isinstance(node, dict) and "item" in node:
        return Has(node["item"], count=node.get("count", 1))

    if isinstance(node, dict) and "category" in node:
        return HasGroup(node["category"], count=node.get("count", 1))

    if isinstance(node, dict) and "function" in node:
        return FUNCTION_TABLE[node["function"]](options, *node.get("args", []))

    raise TypeError(f"Invalid requirement node: {node}")


def parse_requirement(req: str, options: SMBOptions) -> Rule:
    return evaluate_requirement(parse_expression(tokenize(req)), options)


def boss_req(options: SMBOptions, chpt: int) -> Rule:
    return Has(f"Chapter {chpt} Boss Key", count=options.boss_req.value) & Has("Meat Boy")


def speedrun_req(options: SMBOptions, chpt: int) -> Rule:
    return HasAll(*(f"{chpt}-{i} A+ Rank" for i in range(1, 21 if chpt != 6 else 6)))


def larries(options: SMBOptions) -> Rule:
    rule = boss_req(options, 5) & Has("Meat Boy")
    if options.boss_tokens.value and options.goal == "larries":
        rule = rule & Has("Boss Token", count=options.boss_token_req.value)
    return rule


def lw_drfetus(options: SMBOptions) -> Rule:
    rule = Has("Chapter 6 Boss Key", count=options.lw_dr_fetus_req.value)
    if options.boss_tokens.value and options.goal == "light_world":
        rule = rule & Has("Boss Token", count=options.boss_token_req.value)
    return rule


def dw_drfetus(options: SMBOptions) -> Rule:
    rules = [
        HasAll(f"Chapter {chapter} Key", f"{chapter}-{level} A+ Rank")
        for chapter in range(1, 6)
        for level in range(1, 21)
    ]
    rules.extend(HasAll("Chapter 6 Key", "Meat Boy", f"6-{level} A+ Rank") for level in range(1, 6))
    rules.extend(HasAll("Chapter 7 Key", "Bandage Girl", f"7-{level} A+ Rank") for level in range(1, 21))
    rule = AtLeast(85, *rules)
    if options.boss_tokens.value and options.goal == "dark_world":
        rule = rule & Has("Boss Token", count=options.boss_token_req.value)
    return rule


def add_bandages(rules: List[Rule], options: SMBOptions, chpt: int, count: int, dw_rules: List[tuple[Rule, int]]) -> None:
    if str(chpt) not in options.chapters.value:
        return

    chpt_key = Has(f"Chapter {chpt} Key")
    rules.extend([chpt_key] * count)
    if options.dark_world.value:
        for rule, amount in dw_rules:
            rules.extend([chpt_key & rule] * amount)


def bandages(options: SMBOptions, req: int) -> Rule:
    rules: List[Rule] = []
    add_bandages(rules, options, 1, 11, [
        (Has("1-3 A+ Rank"), 1), (Has("1-5 A+ Rank"), 1), (Has("1-10 A+ Rank"), 1),
        (Has("1-13 A+ Rank"), 2), (Has("1-14 A+ Rank"), 1), (Has("1-15 A+ Rank"), 1),
        (Has("1-17 A+ Rank"), 1), (Has("1-19 A+ Rank"), 1),
    ])
    add_bandages(rules, options, 2, 11, [
        (Has("2-4 A+ Rank"), 1), (Has("2-5 A+ Rank"), 2), (Has("2-6 A+ Rank"), 1),
        (Has("2-7 A+ Rank"), 1), (Has("2-10 A+ Rank"), 1), (Has("2-12 A+ Rank"), 1),
        (Has("2-15 A+ Rank"), 1), (Has("2-16 A+ Rank"), 1),
    ])
    add_bandages(rules, options, 3, 8, [
        (CanReachLocation("3-7WZ Tunnel Vision"), 2),
        (CanReachLocation("3-4 Transmissions (Bandage)"), 1), (Has("3-3 A+ Rank"), 1),
        (Has("3-5 A+ Rank"), 1), (Has("3-6 A+ Rank"), 1), (Has("3-7 A+ Rank"), 1),
        (Has("3-8 A+ Rank"), 2), (CanReachLocation("3-14X Step One (Bandage)"), 1),
        (Has("3-16 A+ Rank"), 1), (Has("3-19 A+ Rank"), 1),
    ])
    add_bandages(rules, options, 4, 11, [
        (Has("4-3 A+ Rank"), 1), (Has("4-4 A+ Rank"), 1),
        (CanReachLocation("4-7XWZ MMMMMM"), 2), (Has("4-8 A+ Rank"), 1),
        (Has("4-10 A+ Rank"), 1), (Has("4-14 A+ Rank"), 1),
        (Has("4-18 A+ Rank"), 1), (Has("4-19 A+ Rank"), 1),
    ])
    add_bandages(rules, options, 5, 11, [
        (Has("5-4 A+ Rank"), 1), (Has("5-5 A+ Rank"), 1), (Has("5-8 A+ Rank"), 1),
        (Has("5-10 A+ Rank"), 1), (Has("5-11 A+ Rank"), 1), (Has("5-17 A+ Rank"), 1),
        (Has("5-18 A+ Rank"), 1), (Has("5-20 A+ Rank"), 2),
    ])
    return AtLeast(req, *rules)


def warp_zone(options: SMBOptions, req: int) -> Rule:
    rules: List[Rule] = []
    add_bandages(rules, options, 1, 3, [(Has("1-13 A+ Rank"), 1)])
    add_bandages(rules, options, 2, 3, [(Has("2-5 A+ Rank"), 1)])
    add_bandages(rules, options, 3, 2, [(CanReachLocation("3-7WZ Tunnel Vision"), 1), (Has("3-8 A+ Rank"), 1)])
    add_bandages(rules, options, 4, 3, [(CanReachLocation("4-7XWZ MMMMMM"), 1)])
    add_bandages(rules, options, 5, 3, [(Has("5-20 A+ Rank"), 1)])
    return AtLeast(req, *rules)


FUNCTION_TABLE = {
    "boss_req": boss_req,
    "speedrun_req": speedrun_req,
    "larries": larries,
    "lw_drfetus": lw_drfetus,
    "dw_drfetus": dw_drfetus,
    "bandages": bandages,
    "warp_zone": warp_zone,
}


def set_rules(world: "SMBWorld") -> None:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    for name, data in location_table.items():
        if not is_location_enabled(options, data):
            continue
        
        # Post goal locations
        if options.goal == "larries" and name in ("-5 |>'-'|>", "-0&& (Beat -5 |>'-'|>)"):
            continue
        if options.goal == "light_world" and name in ("-6 |>'-'|>", "N&8^2^%$1`` (Beat -6 |>'-'|>)", "The End (Beat Chapter 6 Light World)"):
            continue
        if options.goal == "dark_world" and name == "The Real End (Beat Chapter 6 Dark World)":
            continue
        if options.goal == "light_world_chapter7" and name in (
            "Suffragette (Beat Chapter 7 Light World)",
            "Girl Boy (Complete The Cotton Alley Light World Deathless)"
        ):
            continue
        if options.goal == "dark_world_chapter7" and name in (
            "Seneca Falls (Beat Chapter 7 Dark World)",
            "Impossible Boy (Complete The Cotton Alley Dark World Deathless)"
        ):
            continue

        req = data.requirement

        world.set_rule(multiworld.get_location(name, player), parse_requirement(req, options))

    connect_regions(multiworld, "Menu", "Initial", player)

    for i in range(1, 6):
        if str(i) in options.chapters.value:
            connect_regions(multiworld, "Menu", f"Chapter {i}", player)
            world.set_rule(multiworld.get_region("Menu", player).exits[-1], Has(f"Chapter {i} Key"))

    if "6" in options.chapters.value:
        connect_regions(multiworld, "Menu", "Chapter 6", player)
        world.set_rule(multiworld.get_region("Menu", player).exits[-1], HasAll("Chapter 6 Key", "Meat Boy"))
    
    if "7" in options.chapters.value:
        chpt_seven_goal = [f"Chapter {i} Key" for i in range(1, 8) if str(i) in options.chapters.value]

        if options.goal in ("light_world_chapter7", "dark_world_chapter7") and not options.boss_tokens.value:
            connect_regions(multiworld, "Menu", "Chapter 7", player)
            world.set_rule(multiworld.get_region("Menu", player).exits[-1], HasAll(*chpt_seven_goal) & Has("Bandage Girl"))
        else:
            connect_regions(multiworld, "Menu", "Chapter 7", player)
            world.set_rule(multiworld.get_region("Menu", player).exits[-1], HasAll("Chapter 7 Key", "Bandage Girl"))

    boss_tokens_amount: int = 0
    
    # First 4 chapters
    for i in range(4):
        if str(i + 1) in options.chapters.value:
            boss_tokens_amount += 1
    
    # Larries
    if "5" in options.chapters.value and options.goal != "larries":
        boss_tokens_amount += 1
    
    # LW Dr. Fetus
    if "6" in options.chapters.value and options.goal != "light_world":
        boss_tokens_amount += 1
    
    # DW Dr. Fetus
    if "6" in options.chapters.value and options.dark_world.value and options.goal != "dark_world":
        boss_tokens_amount += 1
    
    if options.goal == "bandages":
        completion_rule = Has("Bandage", count=options.bandages_amount.value)
    elif options.goal == "achievements":
        completion_rule = Has("Achievement Token", count=options.achievement_tokens.value)
    elif options.goal == "boss_tokens":
        completion_rule = Has("Boss Token", count=boss_tokens_amount)
    elif options.goal == "light_world_chapter7":
        completion_rule = Has("Chapter 7 LW Level Key", count=20)
    elif options.goal == "dark_world_chapter7":
        completion_rule = Has("Chapter 7 DW Level Key", count=20)
    else:
        completion_rule = Has("Victory")

    if options.goal != "boss_tokens" and options.boss_tokens.value:
        completion_rule = completion_rule & Has("Boss Token", count=boss_tokens_amount)

    world.set_completion_rule(completion_rule)
        