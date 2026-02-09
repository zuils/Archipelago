from BaseClasses import Tutorial, ItemClassification
from typing import Any, List, Optional
from worlds.AutoWorld import WebWorld, World
from .items import item_table, item_name_groups, SMBItem
from .locations import location_table
from .options import SMBOptions
from .regions import create_regions
from .rules import set_rules
import re

class SMBWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Super Meat Boy for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["zuils"]
    )]
    
class SMBWorld(World):
    """
    Super Meat Boy is a tough as nails 2D platformer from the creator Edmund McMillen, 
    who you might recognize from games such as The End is Nigh or The Binding of Isaac: Rebirth.
    """
    game = "Super Meat Boy"
    options_dataclass = SMBOptions
    options: SMBOptions
    topology_present = True
    required_client_version = (0, 6, 4)
    web = SMBWeb()
    
    item_name_to_id = {name: data.item_id for name, data in item_table.items()}
    location_name_to_id = {name: data.location_id for name, data in location_table.items()}
    
    for name, data in item_table.items():
        for category in data.category:
            item_name_groups[category].append(name)
    
    # TODO: Fix this once we can get a random starting character to work
    # starting_characters = [i for i in item_table if "StartingCharacters" in i["category"]]
    def generate_early(self):
        # Finalize options to avoid errors
        # Force enable dark world levels if goal is in dark world
        if self.options.goal in ("dark_world", "dark_world_chapter7"):
            self.options.dark_world.value = 1
        
        # If DW Dr. Fetus needs more than 105 boss keys but chapter 7 is disabled, cap it at 105
        # If chapter 7 is disabled and our goal is to complete LW/DW Chapter 7, turn it on
        if not self.options.chapter_seven.value:
            if self.options.dw_dr_fetus_req.value > 105:
                self.options.dw_dr_fetus_req.value = 105
            
            if self.options.goal in ("light_world_chapter7", "dark_world_chapter7"):
                self.options.chapter_seven.value = 1
        
        
        # If starting chapter is 7 but our goal is to complete all of lw/dw chapter 7
        # or chapter 7 levels aren't enabled, select a random chapter
        if (self.options.starting_chpt.value == 7 and
        (not self.options.chapter_seven.value or self.options.goal in ("light_world_chapter7", "dark_world_chapter7"))):
            self.options.starting_chpt.value = self.multiworld.random.randint(1, 6)
            
    def fill_slot_data(self) -> dict:
        return self.options.as_dict("goal", "boss_req", "lw_dr_fetus_req", "dw_dr_fetus_req",
                                    "chapter_keys", "bandages", "dark_world", "chapter_seven",
                                    "starting_chpt", "achievements", "deathless_achievements",
                                    "speedrun_achievements", "xmas", "bandage_fill")
            
    def create_item(self, name: str, classification: Optional[ItemClassification] = None) -> SMBItem:
        data = item_table[name]
        return SMBItem(name, data.classification if classification is None else classification, data.item_id, self.player)
    
    def create_items(self) -> None:
        item_pool: List[SMBItem] = []
        starting_chpt = self.options.starting_chpt.value
        
        if starting_chpt == 7:
            char = "Bandage Girl"
        else:
            char = "Meat Boy"
            
        self.multiworld.push_precollected(self.create_item(char))
        self.multiworld.push_precollected(self.create_item(f"Chapter {starting_chpt} Key"))
        
        # If our goal is to complete LW Dr. Fetus, create Victory event and put it on the boss
        if self.options.goal == "light_world":
            self.multiworld.get_location("6-Boss LW Dr. Fetus", self.player).place_locked_item(self.create_item("Victory"))
            
        # If our goal is to complete DW Dr. Fetus, create Victory event and put it on the boss
        if self.options.goal == "dark_world":
            self.multiworld.get_location("6-Boss DW Dr. Fetus", self.player).place_locked_item(self.create_item("Victory"))
        
        for name, data in item_table.items():
            for _ in range(data.count):
                item = self.create_item(name)
                # Don't put starting character in the item pool
                if item.name == char:
                    continue
                
                # Don't put starting chapter in the item pool
                if item.name == f"Chapter {starting_chpt} Key":
                    continue
                
                # Don't put victory in the item pool
                if item.name == "Victory":
                    continue
                
                # Don't put Chapter 7 LW/DW Level Keys or Bandage Girl 
                # or Chapter 7 A+ Ranks in the pool if Chapter 7 levels are not enabled
                if (
                    not self.options.chapter_seven.value and 
                    "Chapter 7" in data.category
                ):
                    continue
                
                # If dark world levels are off, don't put A+ Ranks from the item pool
                if (
                    not self.options.dark_world.value and
                    "A+ Rank" in data.category
                ):
                    continue
                
                # If our goal is to complete LW Chapter 7, put Chapter 7 LW Level Keys on LW Chapter 7 levels
                # If our goal is not to complete LW Chapter 7, change Chapter 7 LW Level Keys to filler
                if item.name == "Chapter 7 LW Level Key":
                    if self.options.goal == "light_world_chapter7":
                        # all patterns that are 7-<num> Level Name (excludes A+ Ranks)
                        pattern = re.compile(rf"^7-\d+\b(?!X).*?(?<!\(A\+ Rank\))$")
                        location = next(l for l in self.multiworld.get_unfilled_locations(self.player) if pattern.match(l.name))
                        location.place_locked_item(item)

                        continue
                    else:
                        item.classification = ItemClassification.filler


                # If our goal is to complete DW Chapter 7, put Chapter 7 DW Level Keys on DW Chapter 7 levels
                # If our goal is not to complete DW Chapter 7, don't put Chapter 7 DW Level Keys in the pool
                if item.name == "Chapter 7 DW Level Key":
                    if self.options.goal == "dark_world_chapter7":
                        # all patterns that are 7-<num>X Level Name (excludes A+ Ranks)
                        pattern = re.compile(rf"^7-\d+X\b(?!.*\(A\+ Rank\))")
                        location = next(l for l in self.multiworld.get_unfilled_locations(self.player) if pattern.match(l.name))
                        location.place_locked_item(item)

                    continue
                
                
                item_pool.append(item)
        
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        locations_left = total_locations - len(item_pool)

        bandage_ratio = self.options.bandage_fill.value / 100
        bandage_count = int(locations_left * bandage_ratio)
        filler_count = locations_left - bandage_count
        
        print(f"Total Locations: {total_locations}")
        print(f"Item pool size before extra: {len(item_pool)}")
        
        item_pool.extend(self.create_item("Bandage", ItemClassification.useful) for _ in range(bandage_count))
        item_pool.extend(self.create_item("Degraded Bandage", ItemClassification.filler) for _ in range(filler_count)) # Degraded bandages do nothing
        
        self.multiworld.itempool += item_pool
        
        
    def create_regions(self):
        return create_regions(self.multiworld, self.options, self.player)
    
    def set_rules(self):
        return set_rules(self.multiworld, self.options, self.player)