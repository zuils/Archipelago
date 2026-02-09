from typing import Any, List, Dict, Union, TYPE_CHECKING
from .options import SMBOptions
import orjson
import pkgutil

if TYPE_CHECKING:
    from .locations import SMBLocationData


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(
        pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig")
    )


def is_location_enabled(options: SMBOptions, loc_data: "SMBLocationData") -> bool:
    if "Bandage" in loc_data.category and not options.bandages.value:
        return False
    
    if "xmas" in loc_data.category and not options.xmas.value:
        return False
    
    if "Achievements" in loc_data.category and not options.achievements:
        return False
    
    if "Achievements (Deathless)" in loc_data.category and not options.deathless_achievements.value:
        return False
    
    if "Achievements (Speedrun)" in loc_data.category and not options.speedrun_achievements.value:
        return False
    
    if "Chapter 7" in loc_data.region and not options.chapter_seven.value:
        return False
    
    if any(c.startswith("DW") for c in loc_data.category) and not options.dark_world.value:
        return False

    return True
