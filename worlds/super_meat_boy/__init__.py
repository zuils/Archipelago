from BaseClasses import Tutorial, ItemClassification
from typing import Any, List, Optional
from worlds.AutoWorld import WebWorld, World
from .items import item_table, item_name_groups, SMBItem
from .locations import location_table
from .options import SMBOptions, resolve_options
from .regions import create_regions
from .rules import set_rules
from .utils import get_achievements
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
    
    def generate_early(self):
        resolve_options(self)
            
    def fill_slot_data(self) -> dict:
        return self.options.as_dict("goal", "boss_req", "lw_dr_fetus_req", "dw_dr_fetus_req",
                                    "bandages_amount", "boss_tokens", "boss_token_req", "bandages", 
                                    "dark_world", "chapters", "starting_chpt", "starting_char",
                                    "achievements", "deathless_achievements", "speedrun_achievements", 
                                    "achievement_goals", "achievement_tokens", "bandage_fill",
                                    "death_link", "death_link_amnesty")
            
    def create_item(self, name: str, classification: Optional[ItemClassification] = None) -> SMBItem:
        data = item_table[name]
        return SMBItem(name, data.classification if classification is None else classification, data.item_id, self.player)
    
    def create_items(self) -> None:
        item_pool: List[SMBItem] = []
        starting_chpt = self.options.starting_chpt.value
        starting_characters = [
            "Meat Boy",
            "8-Bit Meat Boy",
            "4-Bit Meat Boy",
            "4-Color Meat Boy",
            "Commander Video",
            "Jill",
            "Ogmo",
            "Flywrench",
            "The Kid",
            "Josef",
            "Naija",
            "RunMan",
            "Steve",
            "Meat Ninja",
            "Brownie"
        ]
        
        if starting_chpt == 7:
            char = "Bandage Girl"
        elif starting_chpt == 6:
            char = "Meat Boy"
        else:
            char = starting_characters[self.options.starting_char.value]
            
        self.multiworld.push_precollected(self.create_item(char, ItemClassification.progression))
        self.multiworld.push_precollected(self.create_item(f"Chapter {starting_chpt} Key"))
        
        # Put victory on boss depending on our goal
        if self.options.goal == "larries":
            self.multiworld.get_location("5-Boss Larries Lament", self.player).place_locked_item(self.create_item("Victory"))
        elif self.options.goal == "light_world":
            self.multiworld.get_location("6-Boss LW Dr. Fetus", self.player).place_locked_item(self.create_item("Victory"))
        elif self.options.goal == "dark_world":
            self.multiworld.get_location("6-Boss DW Dr. Fetus", self.player).place_locked_item(self.create_item("Victory"))
        
        # If boss tokens are enabled, put boss tokens on bosses
        if self.options.boss_tokens.value:
            bosses = [
                ("1", "1-Boss Lil' Slugger"),
                ("2", "2-Boss C.H.A.D"),
                ("3", "3-Boss Brownie"),
                ("4", "4-Boss Little Horn")
            ]
            
            if self.options.goal != "larries":
                bosses.append(("5", "5-Boss Larries Lament"))
            
            if self.options.goal != "light_world":
                bosses.append(("6", "6-Boss LW Dr. Fetus"))
            if self.options.goal != "dark_world" and self.options.dark_world.value:
                bosses.append(("6", "6-Boss DW Dr. Fetus"))
                
            for chapter, boss in bosses:
                if chapter in self.options.chapters.value:
                    location = self.multiworld.get_location(boss, self.player).place_locked_item(self.create_item("Boss Token"))
                
        # Achievement tokens
        if self.options.goal == "achievements":
            achievement_locs = get_achievements(self.options, location_table)
            # achievement_locs = [name for name in achievement_locs if name in location_table and is_location_enabled(self.options, location_table)]

            for location in achievement_locs:
                self.multiworld.get_location(location, self.player).place_locked_item(self.create_item("Achievement Token"))
        
        # Put LW/DW Chapter 7 Keys on Chapter 7 levels if our goal is in chapter 7
        # This is done outside of the main for loop to reduce gen time
        if self.options.goal in ("light_world_chapter7", "dark_world_chapter7"):
            unfilled_locations = self.multiworld.get_unfilled_locations(self.player)

            lw_ch7 = []
            dw_ch7 = []

            # All levels that are 7-<num> Level Name (excludes A+ Ranks)
            lw_pattern = re.compile(r"^7-\d+\b(?!X).*?(?<!\(A\+ Rank\))$")
            # All levels that are 7-<num>X Level Name (excludes A+ Ranks)
            dw_pattern = re.compile(r"^7-\d+X\b(?!.*\(A\+ Rank\))")

            for loc in unfilled_locations:
                if lw_pattern.match(loc.name):
                    lw_ch7.append(loc)
                elif dw_pattern.match(loc.name):
                    dw_ch7.append(loc)

            lw_iter = iter(lw_ch7)
            dw_iter = iter(dw_ch7)

            if self.options.goal == "light_world_chapter7":
                for _ in range(len(lw_ch7)):
                    item = self.create_item("Chapter 7 LW Level Key")
                    location = next(lw_iter)
                    location.place_locked_item(item)

            if self.options.goal == "dark_world_chapter7":
                for _ in range(len(dw_ch7)):
                    item = self.create_item("Chapter 7 DW Level Key")
                    location = next(dw_iter)
                    location.place_locked_item(item)
        
        for name, data in item_table.items():
            count = data.count
            
            # Cap Dr. Fetus Keys
            if name == "DW Dr. Fetus Key":
                dr_fetus_cap: int = 0
                if "6" in self.options.chapters.value and self.options.dark_world.value:
                    for chpt in self.options.chapters.value:
                        if chpt == "6":
                            dr_fetus_cap += 5
                        else:
                            dr_fetus_cap += 20
                            
                count = min(count, dr_fetus_cap)
            
            # Cap bandages
            if self.options.goal == "bandages" and name == "Bandage":
                bandages_cap: int = 0
                for i in range(1, 6):
                    if str(i) in self.options.chapters.value:
                        if i == 3:
                            bandages_cap += 8
                            bandages_cap += self.options.dark_world.value * 12
                        else:
                            bandages_cap += 11
                            bandages_cap += self.options.dark_world.value * 9
                            
                count = min(count, bandages_cap)
                
            for _ in range(count):
                item = self.create_item(name)
                # Don't put starting character in the item pool
                if item.name == char:
                    continue
                
                # Don't put starting chapter in the item pool
                if item.name == f"Chapter {starting_chpt} Key":
                    continue
                
                # Skip items with "Extras" category
                if "Extras" in data.category:
                    continue
                
                # Don't put certain chapter items in the pool if they aren't enabled
                if any(
                    not str(i) in self.options.chapters.value and f"Chapter {i}" in data.category
                    for i in range(1, 8)
                ):
                    continue
                
                # If goal is not bandages, skip bandages from being added into the pool
                if self.options.goal != "bandages" and name == "Bandage":
                    continue
                
                # If dark world levels are off, don't put A+ Ranks or DW Dr. Fetus Token in the item pool
                if not self.options.dark_world.value and ("A+ Rank" in data.category or name == "DW Dr. Fetus Token"):
                    continue
                
                # Skip Chapter 7 LW Level Keys if our goal is lw chapter 7, else change them to filler items
                if item.name == "Chapter 7 LW Level Key":
                    if self.options.goal == "light_world_chapter7":
                        continue
                    else:
                        item.classification = ItemClassification.filler

                # Skip Chapter 7 DW Level Keys since we already put them on all the chapter 7 dw levels if needed
                if item.name == "Chapter 7 DW Level Key":
                    continue                
                
                item_pool.append(item)

        locations_left = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        bandage_ratio = self.options.bandage_fill.value / 100
        bandage_count = int(locations_left * bandage_ratio)
        filler_count = locations_left - bandage_count
        
        item_pool.extend(self.create_item("Bandage", ItemClassification.useful) for _ in range(bandage_count))
        item_pool.extend(self.create_item("Degraded Bandage" if self.options.goal == "bandages" else "Bandage", 
                                        ItemClassification.filler) for _ in range(filler_count)) # Filler item does nothing
        
        self.multiworld.itempool += item_pool
        
        
    def create_regions(self):
        return create_regions(self.multiworld, self.options, self.player)
    
    def set_rules(self):
        return set_rules(self.multiworld, self.options, self.player)