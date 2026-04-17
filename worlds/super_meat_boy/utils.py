from typing import Any, List, Dict, Union, TYPE_CHECKING
import orjson
import pkgutil
import re

if TYPE_CHECKING:
    from .locations import SMBLocationData
    from .options import SMBOptions


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(
        pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig")
    )


def is_location_enabled(options: "SMBOptions", loc_data: "SMBLocationData") -> bool:
    if "Bandage" in loc_data.category:
        if not options.bandages.value:
            return False
        
        # same logic as the bandages function in rules.py
        match = re.search(r"bandages\((\d+)\)", loc_data.requirement)
        if match:
            req = int(match.group(1))
            counter: int = 0
            for i in range(1, 6):
                if str(i) in options.chapters.value:
                    if i == 3:
                        counter += 8
                        counter += options.dark_world.value * 12
                    else:
                        counter += 11
                        counter += options.dark_world.value * 9
                        
            if counter < req:
                return False
    
    if "xmas" in loc_data.category: # and not options.xmas.value:
        return False
    
    if "Achievements" in loc_data.category and not options.achievements.value:
        return False
    
    if "Achievements (Deathless)" in loc_data.category and not options.deathless_achievements.value:
        return False
    
    if "Achievements (Speedrun)" in loc_data.category and not options.speedrun_achievements.value:
        return False
    
    chapters_in_loc = [str(i) for i in range(1, 8) if any(f"Chapter {i}" in cat for cat in loc_data.category) or f"Chapter {i}" in loc_data.region]

    if chapters_in_loc and not any(ch in options.chapters.value for ch in chapters_in_loc):
        return False
    
    if (any(c.startswith("DW") for c in loc_data.category) or "Dark World" in loc_data.category) and not options.dark_world.value:
        return False
    
    # Same logic as the warp_zone function in rules.py
    if "Warp Zone" in loc_data.category:
        match = re.search(r"warp_zone\((\d+)\)", loc_data.requirement)
        if match:
            req = int(match.group(1))
        counter: int = 0
        for i in range(1, 6):
            if str(i) in options.chapters.value:
                counter += 3
                counter += options.dark_world.value
        
        if counter < req:
            return False

    return True


def get_achievements(options: "SMBOptions", locations: Dict[str, "SMBLocationData"]) -> List[str]:
    required = set()
    if "normal" in options.achievement_goals.value:
        required.add("Achievements")
    if "speedrun" in options.achievement_goals.value:
        required.add("Achievements (Speedrun)")
    if "deathless" in options.achievement_goals.value:
        required.add("Achievements (Deathless)")

    valid = [f"Chapter {chpt}" for chpt in options.chapters.value]
    if options.bandages.value:
        valid.append("Bandage")
    
    if options.dark_world.value:
        valid.append("Dark World")
    
    # if options.xmas.value:
    #   valid.append("xmas")
    
    valid.append("Warp Zone")

    achievements = set(valid) | required
    locs = []

    for name, data in locations.items():
        if not is_location_enabled(options, data):
            continue
        categories = data.category
        if not required.intersection(categories):
            continue
        if not set(categories).issubset(achievements):
            continue
        locs.append(name)

    return locs