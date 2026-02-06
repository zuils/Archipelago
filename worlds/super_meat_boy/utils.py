from typing import Any, List, Dict, Union, TYPE_CHECKING
import orjson
import pkgutil

if TYPE_CHECKING:
    from .locations import SMBLocationData
    from . import SMBWorld


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(
        pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig")
    )


def is_location_enabled(world: "SMBWorld", loc_data: "SMBLocationData") -> bool:
    if "Bandage" in loc_data.category and not world.options.bandages.value:
        return False
    
    if "xmas" in loc_data.category and not world.options.xmas.value:
        return False
    
    if "Achievements" in loc_data.category and not world.options.achievements.value:
        return False
    
    if "Achievements (Deathless)" in loc_data.category and not world.options.deathless_achievements.value:
        return False
    
    if "Achievements (Speedrun)" in loc_data.category and not world.options.speedrun_achievements.value:
        return False
    
    if "Chapter 7" in loc_data.region and not world.options.chapter_seven.value:
        return False
    
    if any(c.startswith("DW") for c in loc_data.category) and not world.options.dark_world.value:
        return False

    return True
