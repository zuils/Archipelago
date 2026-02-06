from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Region
from .locations import location_table, SMBLocation
from .utils import is_location_enabled

if TYPE_CHECKING:
    from . import SMBWorld

class SMBRegionData(NamedTuple):
    locations: Optional[List[str]]

def create_regions(world: "SMBWorld") -> None:
    region_table: Dict[str, SMBRegionData] = {
        "Menu": SMBRegionData(None),
        "Initial": SMBRegionData([]),
        **{f"Chapter {i}": SMBRegionData([]) for i in range(1, 8)}
    }
    
    # Loop through every location, append to region_table if the option isn't disabled.
    for loc_name, loc_data in location_table.items():
        if not is_location_enabled(world, loc_data):
            continue
        
        region_table[loc_data.region].locations.append(loc_name)
        
    for reg_name, reg_data in region_table.items():
        world.multiworld.regions.append(create_region(world.multiworld, world.player, reg_name, reg_data))

def create_region(multiworld: MultiWorld, player: int, name: str, data: SMBRegionData) -> Region:
    region = Region(name, player, multiworld)
    if data.locations:
        for name in data.locations:
            data = location_table.get(name)
            location = SMBLocation(player, name, data.location_id, region)
            region.locations.append(location)

    return region

def connect_regions(multiworld: MultiWorld, source: str, target: List[str], rule = None) -> None:
    source_region = multiworld.get_region(source)
    target_region = multiworld.get_region(target)
    source_region.connect(target_region, rule=rule)