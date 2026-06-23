# Look at `Rules.dsv` first to get an idea for how this works

import logging
from typing import Union, Tuple, List, Dict, Set
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, ItemClassification, Tutorial, CollectionState
from .Checks import (
    TerrariaItem,
    TerrariaLocation,
    Condition,
    goals,
    rules,
    rule_indices,
    labels,
    rewards,
    item_name_to_id,
    location_name_to_id,
    loc_to_item,
    COND_ITEM,
    COND_LOC,
    COND_FN,
    COND_GROUP,
    npcs,
    pickaxes,
    hammers,
    mech_bosses,
    armor_minions,
    accessory_minions,
    health_upgrades,
    quarter_fruits,
)
from .Options import TerrariaOptions, Goal, ter_option_groups


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


class TerrariaWorld(World):
    """
    Terraria is a 2D multiplayer sandbox game featuring mining, building, exploration, and combat.
    Features 18 bosses and 4 classes.
    """
    game = "Terraria_Desp_Beta"
    web = TerrariaWeb()
    options_dataclass = TerrariaOptions
    options: TerrariaOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    calamity = False
    getfixedboi = False

    progression = set()
    npcs_to_randomize = set()

    ter_items: List[str]
    ter_locations: List[str]

    ter_goals: Dict[str, str]
    goal_items: Set[str]
    goal_locations: Set[str]

    required_client_version = (0, 6, 90)

    def generate_early(self) -> None:
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

        if self.options.getfixedboi and self.options.randomize_npcs:
            logging.warning(f"SLOT {slot_name}: getfixedboi mode was selected with NPC rando enabled; disabling NPC rando")
            self.options.randomize_npcs.value = 0

        for location in goal_locations:
            if location == "Wall of Flesh" and not self.options.randomize_npcs.value:
                logging.warning(
                    f"SLOT {slot_name}: goal 'Wall of Flesh' was enabled was selected with NPC Randomization disabled. The resulting game will be goalable from Sphere 1."
                )
            flags = rules[rule_indices[location]].flags
            if not self.options.calamity.value and "Calamity" in flags:
                logging.warning(
                    f"SLOT {slot_name}: goal `{Goal.name_lookup[self.options.goal.value]}`, which requires Calamity, was selected with Calamity disabled; enabling Calamity"
                )
                self.options.calamity.value = 1

            if "Npc" in flags:
                event = location
            else:
                event = flags.get("Item") or f"Post-{location}"
            ter_goals[event] = location
            goal_items.add(event)

        location_count = 0
        locations = []
        item_count = 0
        items = []

        events = []

        def mark_progression(conditions):
            for condition in conditions:
                if condition.type == COND_ITEM:
                    prog = condition.condition in self.progression
                    self.progression.add(loc_to_item[condition.condition])
                    rule = rules[rule_indices[condition.condition]]
                    if (
                            not prog
                            and "Achievement" not in rule.flags
                            and "Location" not in rule.flags
                            and "Npc" not in rule.flags
                            and "Item" not in rule.flags
                    ):
                        mark_progression(rule.conditions)
                elif condition.type == COND_LOC:
                    mark_progression(rules[rule_indices[condition.condition]].conditions)
                elif condition.type == COND_GROUP:
                    _, conditions = condition.condition
                    mark_progression(conditions)
        valid_rules = rules[:goal] if goal != 0 else rules
        for rule in valid_rules:
            early = "Early" in rule.flags
            rare = "Rare" in rule.flags
            time = "Time" in rule.flags
            crafting = "Crafting" in rule.flags
            grindy = "Grindy" in rule.flags
            fishing = "Fishing" in rule.flags

            if (
                    (not self.options.getfixedboi.value and "Getfixedboi" in rule.flags)
                    or (self.options.getfixedboi.value and "Not Getfixedboi" in rule.flags)
                    or (not self.options.calamity.value and "Calamity" in rule.flags)
                    or (self.options.calamity.value and "Not Calamity" in rule.flags)
                    or (
                            self.options.getfixedboi.value
                            and self.options.calamity.value
                            and "Not Calamity Getfixedboi" in rule.flags
                    )
                    or (not self.options.shimmer_skips.value and "Shimmer" in rule.flags)
                    or (not self.options.early_achievements.value and early)
                    or (
                            not self.options.normal_achievements.value
                            and "Achievement" in rule.flags
                    )
                    or (not self.options.rare_achievements.value and rare)
                    or (not self.options.time_achievements.value and time)
                    or (not self.options.crafting_achievements.value and crafting)
                    or (not self.options.grindy_achievements.value and grindy)
                    or (not self.options.fishing_achievements.value and fishing)
            ) and rule.name not in goal_locations:
                continue

            # Special events
            if (
                    "Npc" in rule.flags
                    or "Pet" in rule.flags
                    or "Pickaxe" in rule.flags
                    or "Hammer" in rule.flags
                    or "Mech Boss" in rule.flags
                    or "Minions" in rule.flags
                    or "Armor Minions" in rule.flags
                    or "Health" in rule.flags
                    or "Quarter Fruit" in rule.flags
                    or rule.name in goal_locations
            ):
                self.progression.add(loc_to_item[rule.name])
                mark_progression(rule.conditions)

            if "Location" in rule.flags or "Achievement" in rule.flags or (
                    "Npc" in rule.flags and self.options.randomize_npcs.value):
                # Location
                location_count += 1
                locations.append(rule.name)
                if "Npc" in rule.flags:
                    self.npcs_to_randomize.add(rule.name)
                mark_progression(rule.conditions)
            elif (
                    "Achievement" not in rule.flags
                    and "Location" not in rule.flags
                    and "Item" not in rule.flags
                    and not ("Npc" in rule.flags and self.options.randomize_npcs.value)
            ):
                # Event
                locations.append(rule.name)
                events.append(rule.name)

            if ("Item" in rule.flags
                or ("Npc" in rule.flags and self.options.randomize_npcs.value)
            ) and not (
                    "Achievement" in rule.flags and rule.name not in goal_locations
            ):
                # Item
                item_count += 1
                if rule.name not in goal_locations:
                    items.append(rule.name)
            elif (
                    "Achievement" not in rule.flags
                    and "Location" not in rule.flags
                    and "Item" not in rule.flags
                    and not ("Npc" in rule.flags and self.options.randomize_npcs.value)
            ):
                # Event
                items.append(rule.name)

        pointless_events = [event for event in events if loc_to_item[event] not in self.progression]
        for event in pointless_events:
            locations.remove(event)
            items.remove(loc_to_item[event])
            location_count -= 1
            item_count -= 1

        ordered_rewards = [
            reward
            for reward in labels["ordered"]
            if self.options.calamity.value or "Calamity" not in rewards[reward]
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
            if self.options.calamity.value or "Calamity" not in rewards[reward]
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
            rule = rules[rule_indices[location]]
            if "Npc" in rule.flags and not self.options.randomize_npcs.value:
                location_id = None
            else:
                location_id = location_name_to_id.get(location)

            menu.locations.append(
                TerrariaLocation(
                    self.player, location, location_id, menu
                )
            )

        self.multiworld.regions.append(menu)

    def create_item(self, item: str) -> TerrariaItem:
        if item in self.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return TerrariaItem(item, classification, item_name_to_id[item], self.player)

    def create_items(self) -> None:
        for item in self.ter_items:
            if (rule_index := rule_indices.get(item)) is not None:
                rule = rules[rule_index]
                if "Item" in rule.flags:
                    name = rule.flags.get("Item") or f"Post-{item}"
                elif "Npc" in rule.flags and self.options.randomize_npcs.value == 1:
                    name = item
                else:
                    continue
            else:
                name = item

            self.multiworld.itempool.append(self.create_item(name))

        locked_items = {}

        for location in self.ter_locations:
            rule = rules[rule_indices[location]]
            if "Location" not in rule.flags and "Achievement" not in rule.flags \
                    and not ("Npc" in rule.flags and self.options.randomize_npcs.value):
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

    def check_condition(self, state, condition: Condition) -> bool:
        if condition.type == COND_ITEM:
            rule = rules[rule_indices[condition.condition]]
            if "Item" in rule.flags:
                name = rule.flags.get("Item") or f"Post-{condition.condition}"
            else:
                name = condition.condition

            return condition.sign == state.has(name, self.player)
        elif condition.type == COND_LOC:
            rule = rules[rule_indices[condition.condition]]
            return condition.sign == self.check_conditions(
                state, rule.operator, rule.conditions
            )
        elif condition.type == COND_FN:
            if condition.condition == "npc":
                if type(condition.argument) is not int:
                    raise Exception("@npc requires an integer argument")

                npc_count = 0
                for npc in npcs:
                    if state.has(npc, self.player):
                        npc_count += 1
                        if npc_count >= condition.argument:
                            return condition.sign

                return not condition.sign
            elif condition.condition == "npc_rando":
                return condition.sign == self.options.randomize_npcs.value
            elif condition.condition == "calamity":
                return condition.sign == self.options.calamity.value
            elif condition.condition == "rare":
                return condition.sign == self.options.rare_achievements.value
            elif condition.condition == "time":
                return condition.sign == self.options.time_achievements.value
            elif condition.condition == "pickaxe":
                if type(condition.argument) is not int:
                    raise Exception("@pickaxe requires an integer argument")

                for pickaxe, power in pickaxes.items():
                    if power >= condition.argument and state.has(pickaxe, self.player):
                        return condition.sign

                return not condition.sign
            elif condition.condition == "hammer":
                if type(condition.argument) is not int:
                    raise Exception("@hammer requires an integer argument")

                for hammer, power in hammers.items():
                    if power >= condition.argument and state.has(hammer, self.player):
                        return condition.sign

                return not condition.sign
            elif condition.condition == "mech_boss":
                if type(condition.argument) is not int:
                    raise Exception("@mech_boss requires an integer argument")

                return state.count_from_list(mech_bosses, self.player) >= condition.argument
            elif condition.condition == "minions":
                if type(condition.argument) is not int:
                    raise Exception("@minions requires an integer argument")

                minion_count = 1
                for armor, minions in armor_minions.items():
                    if state.has(armor, self.player) and minions + 1 > minion_count:
                        minion_count = minions + 1
                        if minion_count >= condition.argument:
                            return condition.sign

                for accessory, minions in accessory_minions.items():
                    if state.has(accessory, self.player):
                        minion_count += minions
                        if minion_count >= condition.argument:
                            return condition.sign

                return not condition.sign
            elif condition.condition == "health":
                if type(condition.argument) is not int:
                    raise Exception("@health requires an integer argument")

                if not self.options.health_logic.value:
                    return condition.sign

                health_required = max(condition.argument + self.options.health_logic_handicap.value, 1)

                for i in range(min(health_required, 2)):
                    if not state.has(health_upgrades[i], self.player):
                        return not condition.sign

                quarter_fruits_required = health_required - 2
                if not self.options.calamity.value or quarter_fruits_required < 1:
                    return condition.sign

                if state.count_from_list(quarter_fruits, self.player) >= quarter_fruits_required:
                     return condition.sign
                else:
                    return not condition.sign

                return condition.sign
            elif condition.condition == "getfixedboi":
                return condition.sign == self.options.getfixedboi.value
            elif condition.condition == "shimmer_skips":
                return condition.sign == self.options.shimmer_skips.value
            else:
                raise Exception(f"Unknown function {condition.condition}")
        elif condition.type == COND_GROUP:
            operator, conditions = condition.condition
            return condition.sign == self.check_conditions(state, operator, conditions)

    def check_conditions(
            self,
            state,
            operator: Union[bool, None],
            conditions: List[
                Tuple[
                    bool,
                    int,
                    Union[str, Tuple[Union[bool, None], list]],
                    Union[str, int, None],
                ]
            ],
    ) -> bool:
        if operator is None:
            if len(conditions) == 0:
                return True
            if len(conditions) > 1:
                raise Exception("Found multiple conditions without an operator")
            return self.check_condition(state, conditions[0])
        elif operator:
            return any(
                self.check_condition(state, condition) for condition in conditions
            )
        else:
            return all(
                self.check_condition(state, condition) for condition in conditions
            )

    def set_rules(self) -> None:
        for location in self.ter_locations:
            def check(state: CollectionState, location=location):
                rule = rules[rule_indices[location]]
                return self.check_conditions(state, rule.operator, rule.conditions)

            self.multiworld.get_location(location, self.player).access_rule = check

        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
            self.goal_items, self.player
        )

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "goal": list(self.goal_locations),
            "deathlink": bool(self.options.death_link),
            "version": list(self.required_client_version),
            # The rest of these are included for trackers
            "calamity": self.options.calamity.value,
            "getfixedboi": self.options.getfixedboi.value,
            "early_achievements": self.options.early_achievements.value,
            "normal_achievements": self.options.normal_achievements.value,
            "grindy_achievements": self.options.grindy_achievements.value,
            "fishing_achievements": self.options.fishing_achievements.value,
            "randomize_npcs": list(self.npcs_to_randomize),
        }
