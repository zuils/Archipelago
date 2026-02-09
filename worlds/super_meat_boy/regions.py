from typing import Dict, List, NamedTuple, Optional
from BaseClasses import MultiWorld, Region
from .locations import location_table, SMBLocation
from .options import SMBOptions
from .utils import is_location_enabled

class SMBRegionData(NamedTuple):
    locations: Optional[List[str]]

def create_regions(world: MultiWorld, options: SMBOptions, player: int) -> None:
    region_table: Dict[str, SMBRegionData] = {
        "Menu": SMBRegionData(None),
        "Initial": SMBRegionData([]),
        **{f"Chapter {i}": SMBRegionData([]) for i in range(1, 8)}
    }
    
    # Loop through every location, append to region_table if the option isn't disabled.
    for loc_name, loc_data in location_table.items():
        if not is_location_enabled(options, loc_data):
            continue
        
        region_table[loc_data.region].locations.append(loc_name)
        
    for reg_name, reg_data in region_table.items():
        world.regions.append(create_region(world, player, reg_name, reg_data))

def create_region(world: MultiWorld, player: int, reg_name: str, reg_data: SMBRegionData) -> Region:
    region = Region(reg_name, player, world)
    if reg_data.locations:
        for loc_name in reg_data.locations:
            data = location_table.get(loc_name)
            location = SMBLocation(player, loc_name, data.location_id, region)
            region.locations.append(location)

    return region

def connect_regions(world: MultiWorld, source: str, target: str, player, rule = None) -> None:
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)
    source_region.connect(target_region, rule=rule)