from BaseClasses import Tutorial, ItemClassification
from typing import List, Optional, Dict
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .items import item_table, PacManWorld2Item
from .locations import location_table
from .options import PacManWorld2Options
from .regions import create_regions
from .rules import set_rules

def launch_client(*args: str) -> None:
    from .client import launch
    launch_subprocess(launch, name="Pac-Man World 2 Client", args=args)

components.append(Component("Pac-Man World 2 Client", func=launch_client, component_type=Type.CLIENT))


class PacManWorld2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Pac-Man World 2 for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["zuils"]
    )]


class PacManWorld2World(World):
    """
    Pac-Man World 2 is a 3D platformer where Pac-Man travels across Pac-Land to recover the Golden Fruit stolen by the ghosts.
    """
    game = "Pac-Man World 2"
    options_dataclass = PacManWorld2Options
    options: PacManWorld2Options
    topology_present = True
    required_client_version = (0, 6, 4)
    web = PacManWorld2Web()
    level_locations: Dict[str, str]
    region_order: List[str]
    goal_location: str
    goal_location_id: Optional[int] = None
    
    item_name_to_id = {name: data.item_id for name, data in item_table.items()}
    location_name_to_id = {name: data.location_id for name, data in location_table.items()}
    
    def write_spoiler(self, spoiler_handle) -> None:
        region_order = getattr(self, "region_order", None)
        if not region_order:
            return

        location_cache = self.multiworld.regions.location_cache[self.player]
        order_index = {region: i for i, region in enumerate(region_order)}

        # Reorder the list of locations in the spoiler log to match the region order.
        reordered = dict(sorted(location_cache.items(), key=lambda pair: order_index.get(pair[1].parent_region.name, len(region_order))))

        location_cache.clear()
        location_cache.update(reordered)
    
    def generate_early(self) -> None:
        # Resolve options to avoid gen errors
        if self.options.total_levels.value == 1:
            self.options.token_goal.value = 0


    def create_item(self, name: str, classification: Optional[ItemClassification] = None) -> PacManWorld2Item:
        data = item_table[name]
        return PacManWorld2Item(name, data.classification if classification is None else classification, data.item_id, self.player)
    
    def create_items(self) -> None:
        item_pool: List[PacManWorld2Item] = []
        
        for name, data in item_table.items():
            count = data.count
            
            if name == "Progressive Level":
                count = self.options.total_levels.value - 1
            
            if name == "Token":
                if self.options.token_goal.value == 0:
                    continue
                else:
                    # We check minimum because if all levels are on then total levels * 2 will produce 1 more than the max because of Pac-Village
                    count = min(data.count, self.options.total_levels.value * 2)
            
            item_pool.extend(self.create_item(name) for _ in range(count))
        
        locations_left: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool.extend(self.create_filler() for _ in range(locations_left))
        
        self.multiworld.itempool += item_pool
    
    def get_filler_item_name(self) -> str:
        return "Pac-Dot"
    
    def create_regions(self) -> None:
        return create_regions(self.multiworld, self.options, self.player)
    
    def set_rules(self) -> None:
        return set_rules(self, self.options, self.player)
    
    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        hint_data[self.player] = {}
        
        # To make hints not complete ass you'll be able to see where the level is in correspondence to the vanilla location.
        for location in self.multiworld.get_locations(self.player):
            if location.address is None:
                continue
            
            vanilla_level = self.level_locations[location.parent_region.name]
            hint_data[self.player][location.address] = vanilla_level
    
    def fill_slot_data(self) -> dict:
        return {
            "token_goal": self.options.token_goal.value,
            "total_levels": self.options.total_levels.value,
            "tokensanity": self.options.tokensanity.value,
            "pacdotsanity": self.options.pacdotsanity.value,
            "time_trials": self.options.time_trials.value,
            #"level_rando": self.options.level_rando.value,
            #"spooky_rando": self.options.spooky_rando.value,
            "death_link": self.options.death_link.value,
            "goal_location": self.goal_location
        }