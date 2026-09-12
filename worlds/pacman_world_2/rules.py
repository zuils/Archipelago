from typing import Dict, List, TYPE_CHECKING
from BaseClasses import ItemClassification, CollectionState
from rule_builder.rules import Has, CanReachLocation, And, Or
from .options import PacManWorld2Options
from .items import PacManWorld2Item
from .locations import location_table, PacManWorld2Location
from .regions import connect_regions

if TYPE_CHECKING:
    from . import PacManWorld2World

def set_rules(world: "PacManWorld2World", options: PacManWorld2Options, player: int) -> None:
    # Keep region order from location_table while removing duplicates.
    all_regions: List[str] = list(dict.fromkeys(data.region for data in location_table.values()))
    vanilla_order: List[str] = list(all_regions)
    shuffled_regions: List[int] = []
    
    region_is_boss: Dict[str, bool] = {data.region: data.is_boss for data in location_table.values()}
    
    # Only levels
    if options.level_rando.value == 1:
        shuffled_regions = [i for i, region in enumerate(all_regions) if not region_is_boss[region]]
    # Only bosses 
    elif options.level_rando.value == 2:
        shuffled_regions = [i for i, region in enumerate(all_regions) if region_is_boss[region]]
        # Spooky will appear at the end of the list
        if not options.spooky_rando:
            del shuffled_regions[-1]
    # Both levels and bosses
    elif options.level_rando.value == 3:
        shuffled_regions = list(range(len(all_regions)))
        if not options.spooky_rando:
            del shuffled_regions[-1]
    
    if shuffled_regions:
        vals: List[str] = [all_regions[i] for i in shuffled_regions]
        world.random.shuffle(vals)
        
        for i, val in zip(shuffled_regions, vals):
            all_regions[i] = val

    # Keep track of how the levels are ordered so we can extend the hint information and not have a bad apworld.
    world.level_locations = {region: vanilla_order[i] for i, region in enumerate(all_regions)}
    world.region_order = all_regions
    
    connect_regions(world, "Menu", all_regions[0])
    prev_region: str = all_regions[0]
    level_reqs: int = 1
    for region in all_regions[1:]:
        rule = Has("Progressive Level", level_reqs)
        
        if region == all_regions[-1]:
            rule = And(rule, Has("Token", options.token_goal.value))
        
        connect_regions(world, prev_region, region, rule)

        prev_region = region
        level_reqs += 1
    
    final_region = all_regions[-1]

    if region_is_boss[final_region]:
        final_location = next(name for name, data in location_table.items() if data.region == final_region)
        victory_name = final_location.split(": ", 1)[1]
    else:
        final_location = f"{final_region}: Level Complete"
        victory_name = f"Complete {final_region}"
        
    final_region = world.get_region(final_region)
    victory_loc = PacManWorld2Location(player, victory_name, None, final_region)
    victory_loc.access_rule = lambda state: state.can_reach_location(final_location, player)
    victory_loc.place_locked_item(PacManWorld2Item("Victory", ItemClassification.progression, None, player))
    final_region.locations.append(victory_loc)
        
    world.set_completion_rule(Has("Victory"))