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
    
    def generate_early(self):
        # Finalize options to avoid errors        
        # Force chapter 6 and 7 levels to be on if our goal is in chapter 7
        if self.options.goal in ("light_world_chapter7", "dark_world_chapter7"):
            self.options.chapter_six.value = 1
            self.options.chapter_seven.value = 1
        # Force chapter 6 levels if our goal is either lw/dw dr. fetus or in chapter 7
        elif self.options.goal not in ("larries", "bandages"):
            self.options.chapter_six.value = 1
        
        # Force chapter 7 levels to be disabled if we don't have chapter 7 levels enabled
        if not self.options.chapter_six.value:
            self.options.chapter_seven.value = 0
            
        # Likewise do the opposite
        if self.options.chapter_seven.value:
            self.options.chapter_six.value = 1
            
        # Force dark world levels enabled if our goal is in dark world
        if self.options.goal in ("dark_world", "dark_world_chapter7"):
            self.options.dark_world.value = 1
            
        # Set bandage fill to 0 if our goal isn't bandages
        if self.options.goal != "bandages":
            self.options.bandage_fill.value = 0
            
        # Cap DW Dr. Fetus Keys Amount if we don't have chapter 6/7 levels enabled
        if not self.options.chapter_six.value:
            self.options.dw_dr_fetus_req.value = min(self.options.dw_dr_fetus_req.value, 100)
        elif not self.options.chapter_seven.value:
            self.options.dw_dr_fetus_req.value = min(self.options.dw_dr_fetus_req.value, 105)
            
        # Cap Bandages if dark world levels aren't enabled
        if self.options.goal == "bandages" and not self.options.dark_world.value:
            self.options.bandages_amount.value = min(self.options.dark_world.value, 52)

        # If starting chapter is 7 but our goal is to complete all of lw/dw chapter 7
        # or chapter 7 levels aren't enabled, select a random chapter
        if (self.options.starting_chpt.value == 7 and
        (not self.options.chapter_seven.value or self.options.goal in ("light_world_chapter7", "dark_world_chapter7"))):
            self.options.starting_chpt.value = self.multiworld.random.randint(1, 6)
            
    def fill_slot_data(self) -> dict:
        return self.options.as_dict("goal", "boss_req", "lw_dr_fetus_req", "dw_dr_fetus_req",
                                    "bandages_amount", "boss_tokens", "bandages", "dark_world", 
                                    "chapter_six", "chapter_seven", "starting_chpt", "starting_char", 
                                    "achievements", "deathless_achievements", "speedrun_achievements", 
                                    "xmas", "bandage_fill")
            
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
            "Meat Ninja"
        ]
        
        if starting_chpt == 7:
            char = "Bandage Girl"
        elif starting_chpt == 6:
            char = "Meat Boy"
        else:
            char = starting_characters[self.options.starting_char.value]
            
        self.multiworld.push_precollected(self.create_item(char))
        self.multiworld.push_precollected(self.create_item(f"Chapter {starting_chpt} Key"))
        
        if self.options.debug.value:
            highest = 5
            
            if self.options.chapter_six.value:
                highest += 1
            
            if self.options.chapter_seven.value:
                highest += 1
                
            for i in range(1, highest + 1):
                for j in range(1, 21 if i != 6 else 6):
                    self.multiworld.push_precollected(self.create_item(f"{i}-{j} A+ Rank"))
        
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
                "1-Boss Lil' Slugger",
                "2-Boss C.H.A.D",
                "3-Boss Brownie",
                "4-Boss Little Horn"
            ]
            
            if self.options.goal != "larries":
                bosses.append("5-Boss Larries Lament")
            
            if self.options.chapter_six.value:
                if self.options.goal != "light_world":
                    bosses.append("6-Boss LW Dr. Fetus")

                if self.options.goal != "dark_world" and self.options.dark_world.value:
                    bosses.append("6-Boss DW Dr. Fetus")
                
            for boss in bosses:
                location = self.multiworld.get_location(boss, self.player).place_locked_item(self.create_item("Boss Token"))
        
        for name, data in item_table.items():
            count = data.count
            # If chapter 7 is disabled, change DW Dr. Fetus Key count
            if not self.options.chapter_seven.value and name == "DW Dr. Fetus Key":
                count = 105
            
            # If chapter 6 is disabled, change DW Dr. Fetus Key count
            if not self.options.chapter_six.value and name == "DW Dr. Fetus Key":
                count = 100
                
            # Cap bandages if dark world levels are disabled
            if self.options.goal == "bandages" and not self.options.dark_world.value and name == "Bandage":
                count = 52
                
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
                
                # If Chapter 6 is off, don't put chapter 6 items into the pool
                if not self.options.chapter_six.value and "Chapter 6" in data.category:
                    continue
                
                # If Chapter 7 is off, don't put chapter 7 items into the pool
                if not self.options.chapter_seven.value and "Chapter 7" in data.category:
                    continue
                
                # If goal is not bandages, skip bandages from being added into the pool
                if self.options.goal != "bandages" and name == "Bandage":
                    continue
                
                # If dark world levels are off, don't put A+ Ranks or DW Dr. Fetus Key in the item pool
                if not self.options.dark_world.value and (
                    "A+ Rank" in data.category or name == "DW Dr. Fetus Key"):
                    continue
                
                if self.options.debug.value and "A+ Rank" in data.category:
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