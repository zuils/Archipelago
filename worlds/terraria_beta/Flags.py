# Manages flag logic & behavior for the parser and multiworld
from typing import List, Tuple

from .Options import TerrariaOptions

rule_flags = [
    "Location",  # Standard core locations
    "Item",  # Standard core items
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
    "Shimmer",  # Unique flag for Aether access + shimmer logic
    "Health",
    "Quarter Fruit",
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

def is_location_is_item(flags: List[str], options: TerrariaOptions) -> Tuple[bool, bool]:
    if "Npc" in flags and options.randomize_npcs.value == 1:
        return True, True
    else:
        return is_location_only(flags), is_item_only(flags, options)


def is_location_only(flags: List[str]) -> bool:
    return ("Location" in flags
            or "Achievement" in flags)

def is_item_only(flags: List[str], options: TerrariaOptions) -> bool:
    return "Item" in flags
