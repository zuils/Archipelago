from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import MultiWorld, Region
from .locations import PacManWorld2Location, location_table

if TYPE_CHECKING:
    from . import PacManWorld2World
    from .options import PacManWorld2Options


class PacManWorld2RegionData(NamedTuple):
    locations: Optional[List[str]]


def create_regions(world: MultiWorld, options: "PacManWorld2Options", player: int) -> None:
    region_table: Dict[str, PacManWorld2RegionData] = {
        "Menu": PacManWorld2RegionData(None)
    }
    
    pacdots: Dict[str, List[str]] = {}
    
    for name, data in location_table.items():
        if "Token" in name and not options.tokensanity:
            continue
        
        if name.startswith(f"{data.region}: Pac-Dot"):
            pacdots.setdefault(data.region, []).append(name)
        else:
            region_table.setdefault(data.region, PacManWorld2RegionData([])).locations.append(name)
    
    size: int = options.pacdotsanity.value
    if size:
        for region, names in pacdots.items():
            bundles, remainder = divmod(len(names), size)
            selected = [names[(i + 1) * size - 1] for i in range(bundles)]
            if remainder:
                selected.append(names[-1])  # leftover partial bundle keeps the real final dot's number
            for name in selected:
                region_table[region].locations.append(name)
    
    for name, data in region_table.items():
        world.regions.append(create_region(world, player, name, data))

def create_region(world: MultiWorld, player: int, region_name: str, region_data: PacManWorld2RegionData) -> Region:
    region = Region(region_name, player, world)
    if region_data.locations:
        for loc_name in region_data.locations:
            data = location_table.get(loc_name)
            location = PacManWorld2Location(player, loc_name, data.location_id, region)
            region.locations.append(location)
    
    return region

def connect_regions(world: "PacManWorld2World", source: str, target: str, rule = None) -> None:
    source_region = world.get_region(source)
    target_region = world.get_region(target)
    source_region.connect(target_region, rule=rule)