# Look at `Rules.dsv` first to get an idea for how this works

import dataclasses
import logging
from typing import Union, Tuple, List, Dict, Set, override

from Options import NumericOption
from rule_builder.cached_world import CachedRuleBuilderWorld
from rule_builder.field_resolvers import FromWorldAttr
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, ItemClassification, Tutorial, CollectionState, Spoiler, MultiWorld
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasAll, True_, False_, And, Or, Rule, TWorld, HasFromList, Filtered, \
    HasAnyCount, NestedRule
from .Flags import (
    invalid_flag,
    is_location_is_item, list_flags, tuple_list_flags
)
from .Checks import (
    game_name,
    TerrariaItem,
    TerrariaLocation,
    Condition,
    goals,
    entries,
    entry_indices,
    labels,
    rewards,
    item_name_to_id,
    location_name_to_id,
    loc_to_item,
    flag_to_items,
    COND_ITEM,
    COND_LOC,
    COND_FN,
    COND_GROUP, OUT_OF_LOGIC,
)
from .Options import TerrariaOptions, Goal, ter_option_groups, RandomizeNPCs, Mods, RareAchievements, \
    TimeAchievements, HealthLogic, Getfixedboi, ShimmerSkips, FishingSkips, RandomizeDepth


class TerrariaWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Terraria randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Seldom"],
        )
    ]
    option_groups = ter_option_groups


class TerrariaSpoiler(Spoiler):
    def hidden_locations(self) -> Set[str]:
        hidden = set()

        for loc in self.multiworld.get_filled_locations():
            if self.multiworld.game[loc.player] != "Terraria Beta":
                continue

            options = self.multiworld.worlds[loc.player].options
            if not options.compressed_playthrough.value or not loc.is_event:
                continue

            entry = entries[entry_indices[loc.name]]
            if options.health_logic.value and ("Health" in entry.flags or "Quarter Fruit" in entry.flags):
                continue

            hidden.add(loc.name + f" ({self.multiworld.get_player_name(loc.player)})" if self.multiworld.players > 1 else loc.name)

        return hidden

    def create_playthrough(self, create_paths: bool = True) -> None:
        super().create_playthrough(create_paths)

        hidden_locs = self.hidden_locations()

        visible_spheres = []

        for sphere in sorted(int(num) for num in self.playthrough if num != "0"):
            sphere = self.playthrough[str(sphere)]
            visible = {
                loc: item
                for loc, item in sphere.items()
                if loc not in hidden_locs
            }

            if visible:
                visible_spheres.append(visible)

        self.playthrough = {
            "0": self.playthrough.get("0", []),
            **{
                str(num): sphere
                for num, sphere in enumerate(visible_spheres, start=1)
            },
        }

        if create_paths:
            self.paths = {
                location: path
                for location, path in self.paths.items()
                if location not in hidden_locs
            }


class TerrariaWorld(CachedRuleBuilderWorld):
    """
    Terraria is a 2D multiplayer sandbox game featuring mining, building, exploration, and combat.
    Features 18 bosses and 4 classes.
    """
    game = game_name
    web = TerrariaWeb()
    options_dataclass = TerrariaOptions
    options: TerrariaOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    item_name_groups = {
        "Flags": set(flag_to_items["Item"]),
        "NPCs": set(flag_to_items["Npc"]),
        "Rewards": set(rewards.keys()),
    }

    location_name_groups = {
        "Bosses and Events": set(flag_to_items["Location"]),
        "Achievements": set(flag_to_items["Achievement"]).union(set(flag_to_items["Depth Achievement"])),
        "NPCs": set(flag_to_items["Npc"]),
    }

    entries = entries
    entry_indices = entry_indices

    calamity = False
    fargo = False
    getfixedboi = False

    is_ut = False
    ut_can_gen_without_yaml = True

    required_client_version = (0, 6, 200)

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.progression = set()
        self.npcs_to_randomize = set()

        self.ter_items: List[str]
        self.ter_locations: List[str]
        self.bad_events = set()
        self.ter_rules = dict()

        self.ter_goals: Dict[str, str]
        self.goal_items: Set[str]
        self.goal_locations: Set[str]

    # Yamlless UT Support
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, object]) -> Dict[str, object]:
        return {
            "goal": slot_data["goal_option"],
            "shuffle_to": slot_data["shuffle_to_option"],
            "death_link": slot_data["deathlink"],
            "mods": slot_data["mods"],
            "getfixedboi": slot_data["getfixedboi"],
            "randomize_npcs": slot_data["npc_rando"],
            "randomize_depth": slot_data["depth_rando"],
            "early_achievements": slot_data["early_achievements"],
            "normal_achievements": slot_data["normal_achievements"],
            "rare_achievements": slot_data["rare_achievements"],
            "time_achievements": slot_data["time_achievements"],
            "crafting_achievements": slot_data["crafting_achievements"],
            "grindy_achievements": slot_data["grindy_achievements"],
            "fishing_achievements": slot_data["fishing_achievements"],
            "fill_extra_checks_with": slot_data["fill_extra_checks_with"],
            "fishing_skips": slot_data["fishing_skips"],
            "shimmer_skips": slot_data["shimmer_skips"],
            "health_logic": slot_data["health_logic"],
            "health_logic_handicap": slot_data["health_logic_handicap"],
        }
    
    def generate_early(self) -> None:
        self.is_ut = getattr(self.multiworld, "generation_is_fake", False)
        
        # UT passes the connected slot's options through re_gen_passthrough when
        # generating the world without a YAML. Restore those options before generation.
        passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        
        if self.game in passthrough:
            slot_data = passthrough[self.game]

            for option_name, value in slot_data.items():
                if option_name not in self.options_dataclass.type_hints:
                    continue
                
                option_type = self.options_dataclass.type_hints[option_name]
                setattr(self.options, option_name, option_type.from_any(value))
        
        if not isinstance(self.multiworld.spoiler, TerrariaSpoiler):
            self.multiworld.spoiler = TerrariaSpoiler(self.multiworld)
        
        self.glitches_item_name = OUT_OF_LOGIC

        goal, goal_locations = goals[self.options.goal.value]
        slot_name = self.multiworld.player_name[self.player]
        match self.options.shuffle_to.value:
            case 0:
                pass
            case -1:
                goal = 0
            case _:
                if self.options.shuffle_to.value < self.options.goal.value:
                    logging.warning(f"SLOT {slot_name}: \"Shuffle To\" value ({Goal.name_lookup[self.options.shuffle_to.value]}) was set earlier than the goal ({Goal.name_lookup[self.options.goal.value]}); ignoring")
                else:
                    goal, _ = goals[self.options.shuffle_to.value]
        ter_goals = {}
        goal_items = set()

        for location in goal_locations:
            if location == "Wall of Flesh" and not self.options.randomize_npcs.value:
                logging.warning(
                    f"SLOT {slot_name}: goal 'Wall of Flesh' was enabled was selected with NPC Randomization disabled. The resulting game will be goalable from Sphere 1."
                )
            flags = entries[entry_indices[location]].flags
            if "Calamity" not in self.options.mods.value and "Calamity" in flags:
                logging.warning(
                    f"SLOT {slot_name}: goal `{Goal.name_lookup[self.options.goal.value]}`, which requires Calamity, was selected with Calamity disabled; enabling Calamity"
                )
                self.options.mods.value.add("Calamity")
            if "Fargo" not in self.options.mods.value and "Fargo" in flags:
                logging.warning(
                    f"SLOT {slot_name}: goal `{Goal.name_lookup[self.options.goal.value]}`, which requires Fargo, was selected with Fargo disabled; enabling Fargo"
                )
                self.options.mods.value.add("Fargo")

            if "Npc" in flags:
                event = location
            else:
                event = flags.get("Item") or f"Post-{location}"
            ter_goals[event] = location
            goal_items.add(event)

        if self.options.fishing_achievements and not self.options.fishing_skips:
            logging.warning(f"SLOT {slot_name}: fishing achievements are enabled with fishing skips disabled; enabling fishing skips")
            self.options.fishing_skips.value = 1

        if self.options.getfixedboi:
            incompatible_options = []
            if "Princess" in goal_items:
                incompatible_options.append("Princess goal")
            if self.options.randomize_npcs:
                incompatible_options.append("NPC Randomization")
            if "Fargo" in self.options.mods.value:
                incompatible_options.append("Fargo")
            if self.options.randomize_depth:
                incompatible_options.append("Depth Randomization")

            if incompatible_options:
                logging.warning(f"SLOT {slot_name}: getfixedboi mode is enabled with the following incompatible options:\n"
                                f" - {'\n - '.join(incompatible_options)}\n"
                                f"Disabling getfixedboi.")
                self.options.getfixedboi.value = 0

        location_count = 0
        locations = []
        item_count = 0
        items = []

        events = []

        valid_entries = entries[:goal] if goal != 0 else entries
        for entry in valid_entries:

            if invalid_flag(entry.flags, self.options) and entry.name not in goal_locations:
                continue

            built_rule = entry.rule.resolve(self)
            self.ter_rules[entry.name] = built_rule

            is_loc, is_item = is_location_is_item(entry.flags, self.options)

            if is_loc:
                location_count += 1
                locations.append(entry.name)
                if "Npc" in entry.flags:
                    self.npcs_to_randomize.add(entry.name)
            if is_item and not ("Achievement" in entry.flags and entry.name not in goal_locations):
                # Item
                item_amount = next((amount for item, amount in flag_to_items["Progressive Item"] if item == entry.name), 1)
                for i in range(item_amount):
                    item_count += 1
                    if entry.name not in goal_locations:
                        items.append(entry.name)
            elif not is_loc and not is_item:
                # Event
                locations.append(entry.name)
                events.append(entry.name)
                items.append(entry.name)

        # This block evaluates for bad events, or events that will always be false
        # given the current option configuration.
        # See also: The custom HasValid rule
        while True:
            new_baddies = set()
            for name in self.ter_rules.keys():
                if name in self.bad_events:
                    continue
                item_dependents = self.ter_rules[name].item_dependencies().keys()
                if self.bad_events.intersection(item_dependents):
                    self.ter_rules[name] = entries[entry_indices[name]].rule.resolve(self)
                if self.ter_rules[name].always_false:
                    new_baddies.add(name)
            if not new_baddies:
                break
            self.bad_events.update(new_baddies)


        bad_locs = set()
        for loc in locations:
            if loc not in events:
                self.ter_rules[loc] = entries[entry_indices[loc]].rule.resolve(self)
                if self.ter_rules[loc].always_false:
                    bad_locs.add(loc)

        if bad_locs:
            logging.warning(f"SLOT {slot_name}: The following locations are inaccessible due to your config and will be removed:\n"
                            f" - {'\n - '.join(bad_locs)}")


        def mark_progression(rule: Rule.Resolved):
            item_deps = list(rule.item_dependencies().keys())
            while item_deps:
                next_item = item_deps.pop(0)
                if next_item in self.progression:
                    continue
                self.progression.add(next_item)
                if next_item in events:
                    for itm in self.ter_rules[next_item].item_dependencies().keys():
                        item_deps.append(itm)

        for name in goal_locations:
            self.progression.add(loc_to_item[name])
            mark_progression(self.ter_rules[name])

        location_count -= len(bad_locs)
        locations = [loc for loc in locations if (loc not in bad_locs and loc not in self.bad_events)]
        for loc in locations:
            if loc not in events:
                mark_progression(self.ter_rules[loc])
        events = [i for i in events if i not in self.bad_events]
        items = [i for i in items if i not in self.bad_events]

        pointless_events = [event for event in events if loc_to_item[event] not in self.progression]
        for event in pointless_events:
            locations.remove(event)
            items.remove(loc_to_item[event])
            location_count -= 1
            item_count -= 1

        ordered_rewards = [
            reward
            for reward in labels["ordered"]
            if ("Calamity" in self.options.mods.value or "Calamity" not in rewards[reward])
            and ("Fargo" in self.options.mods.value or "Fargo" not in rewards[reward])
        ]
        while (
                self.options.fill_extra_checks_with.value == 1
                and item_count < location_count
                and ordered_rewards
        ):
            items.append(ordered_rewards.pop(0))
            item_count += 1

        random_rewards = [
            reward
            for reward in labels["random"]
            if ("Calamity" in self.options.mods.value or "Calamity" not in rewards[reward])
            and ("Fargo" in self.options.mods.value or "Fargo" not in rewards[reward])
        ]
        self.multiworld.random.shuffle(random_rewards)
        while (
                self.options.fill_extra_checks_with.value == 1
                and item_count < location_count
                and random_rewards
        ):
            items.append(random_rewards.pop(0))
            item_count += 1

        while item_count < location_count:
            items.append("Reward: Coins")
            item_count += 1

        self.ter_items = items
        self.ter_locations = locations

        self.ter_goals = ter_goals
        self.goal_items = goal_items
        self.goal_locations = goal_locations

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)

        for location in self.ter_locations:
            entry = entries[entry_indices[location]]
            is_location, is_item = is_location_is_item(entry.flags, self.options)
            if is_location:
                location_id = location_name_to_id.get(location)
            else:
                location_id = None

            menu.locations.append(
                TerrariaLocation(
                    self.player, location, location_id, menu
                )
            )

        self.multiworld.regions.append(menu)

    def create_item(self, name: str) -> TerrariaItem:
        if name in self.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return TerrariaItem(name, classification, item_name_to_id[name], self.player)

    def create_items(self) -> None:
        for item in self.ter_items:
            if (entry_index := entry_indices.get(item)) is not None:
                entry = entries[entry_index]
                _, is_item = is_location_is_item(entry.flags, self.options)
                if "Item" in entry.flags:
                    name = entry.flags.get("Item") or f"Post-{item}"
                elif is_item:
                    name = item
                else:
                    continue
            else:
                name = item

            self.multiworld.itempool.append(self.create_item(name))

        locked_items = {}

        for location in self.ter_locations:
            entry = entries[entry_indices[location]]
            is_loc, _ = is_location_is_item(entry.flags, self.options)
            if not is_loc:
                if location in self.progression:
                    classification = ItemClassification.progression
                else:
                    classification = ItemClassification.useful

                locked_items[location] = TerrariaItem(
                    location, classification, None, self.player
                )

        for item, location in self.ter_goals.items():
            locked_items[location] = self.create_item(item)
        for location, item in locked_items.items():
            self.multiworld.get_location(location, self.player).place_locked_item(item)


    def set_rules(self) -> None:
        for location_name in self.ter_locations:
            location = self.multiworld.get_location(location_name, self.player)
            self.set_rule(location, entries[entry_indices[location_name]].rule)
        
        # UT won't recognize you're in go mode because it checks if you have the Post-Boss flags.
        # To fix this we check if we can reach the goal locations.
        if self.is_ut:
            self.set_completion_rule(lambda state: all(state.can_reach_location(loc, self.player) for loc in self.goal_locations))
        else:
            self.set_completion_rule(HasAll(*self.goal_items))

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "goal": list(self.goal_locations),
            "deathlink": bool(self.options.death_link),
            "version": list(self.required_client_version),
            "mods": list(self.options.mods.value),
            "calamity": int("Calamity" in self.options.mods.value),
            "fargo": int("Fargo" in self.options.mods.value),
            "getfixedboi": self.options.getfixedboi.value,
            "npc_rando": self.options.randomize_npcs.value,
            "randomize_npcs": list(self.npcs_to_randomize),
            "depth_rando": self.options.randomize_depth.value,
            "goal_option": self.options.goal.value,
            "shuffle_to_option": self.options.shuffle_to.value,
            "early_achievements": self.options.early_achievements.value,
            "normal_achievements": self.options.normal_achievements.value,
            "rare_achievements": self.options.rare_achievements.value,
            "time_achievements": self.options.time_achievements.value,
            "crafting_achievements": self.options.crafting_achievements.value,
            "grindy_achievements": self.options.grindy_achievements.value,
            "fishing_achievements": self.options.fishing_achievements.value,
            "fill_extra_checks_with": self.options.fill_extra_checks_with.value,
            "fishing_skips": self.options.fishing_skips,
            "shimmer_skips": self.options.shimmer_skips.value,
            "health_logic": self.options.health_logic.value,
            "health_logic_handicap": self.options.health_logic_handicap.value,
        }