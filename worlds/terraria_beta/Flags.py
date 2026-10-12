# Manages flag logic & behavior for the parser and multiworld
from typing import List, Tuple

from .Options import TerrariaOptions

rule_flags = [
    "Location",  # Standard core locations
    "Item",  # Standard core items
    "Progressive Item",
    "Goal",
    "Early",  # Achievement + logic modifier
    "Achievement",
    "Rare",  # Achievement + logic modifier
    "Time",  # Achievement + logic modifier
    "Crafting",  # Achievement + logic modifier
    "Grindy",  # Achievement + logic modifier
    "Fishing",  # Achievement + logic modifier
    "Npc",  # Contributes towards NPC counting, Location + Item with NPC Rando enabled
    "Pet",  # Contributes towards NPC counting
    "Pickaxe",  # Paired with tool power
    "Hammer",  # Paired with tool power
    "Minions",  # Paired with additional minion capacity
    "Armor Minions",  # Paired with additional minion capacity, cannot be stacked with other armors
    "Mech Boss",
    "Final Boss",
    "Getfixedboi",
    "Not Getfixedboi",
    "Calamity",
    "Not Calamity",
    "Not Calamity Getfixedboi",
    "Fargo",
    "Not Fargo",
    "Health",
    "Quarter Fruit",
    "Depth",
]

# Flags that indicate the attached event may be necessary for progression
special_events = [
    "Npc",
    "Pet",
    "Pickaxe",
    "Hammer",
    "Mech Boss",
    "Minions",
    "Armor Minions",
    "Health",
    "Quarter Fruit",
]

def invalid_flag(flags: List[str], options: TerrariaOptions):
    for flag in flags:
        valid_flag = True
        match flag:
            case "Getfixedboi":
                valid_flag = options.getfixedboi.value
            case "Not Getfixedboi":
                valid_flag = not options.getfixedboi.value
            case "Calamity":
                valid_flag = "Calamity" in options.mods.value
            case "Not Calamity":
                valid_flag = "Calamity" not in options.mods.value
            case "Not Calamity Getfixedboi":
                valid_flag = "Calamity" not in options.mods.value or not options.getfixedboi.value
            case "Fargo":
                valid_flag = "Fargo" in options.mods.value
            case "Not Fargo":
                valid_flag = "Fargo" not in options.mods.value
            case "Early":
                valid_flag = options.early_achievements.value
            case "Achievement":
                valid_flag = options.normal_achievements.value
            case "Rare":
                valid_flag = options.rare_achievements.value
            case "Time":
                valid_flag = options.time_achievements.value
            case "Crafting":
                valid_flag = options.crafting_achievements.value
            case "Grindy":
                valid_flag = options.grindy_achievements.value
            case "Fishing":
                valid_flag = options.fishing_achievements.value
            case "Depth":
                valid_flag = options.randomize_depth.value
        if not valid_flag:
            return True
    return False

def is_location_is_item(flags: List[str], options: TerrariaOptions | None = None) -> Tuple[bool, bool]:
    if "Npc" in flags and (bool(options.randomize_npcs.value) if options else True):
        return True, True
    else:
        return is_location_only(flags, options), is_item_only(flags)

def is_location_only(flags: List[str], options: TerrariaOptions | None = None) -> bool:
    for flag in flags:
        match flag:
            case "Location":
                return True
            case "Achievement":
                return True
    return False

def is_item_only(flags: List[str]) -> bool:
    return "Item" in flags or "Progressive Item" in flags
