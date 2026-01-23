from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions, Toggle, DefaultOnToggle


class Calamity(Toggle):
    """Calamity mod bosses and events are shuffled"""

    display_name = "Calamity Mod Integration"

class Fargo(Toggle):
    """
    Fargo Souls mod bosses and events are shuffled
    If Calamity is enabled, the Fargo Souls DLC is expected to be on
    """
    
    display_name = "Fargo Souls Integration"

class Getfixedboi(Toggle):
    """Generation accomodates the secret, very difficult "getfixedboi" seed"""

    display_name = """"getfixedboi" Seed"""


class Goal(Choice):
    """
    The victory condition for your run. Stuff after the goal will not be shuffled.
    Primordial Wyrm and Boss Rush are accessible relatively early, so consider "Items" or
    "Locations" accessibility to avoid getting stuck on the goal.
    """

    display_name = "Goal"
    option_mechanical_bosses = 0
    option_calamitas_clone = 1
    option_plantera = 2
    option_golem = 3
    option_empress_of_light = 4
    option_lunatic_cultist = 5
    option_astrum_deus = 6
    option_moon_lord = 7
    option_providence_the_profaned_goddess = 8
    option_devourer_of_gods = 9
    option_eridanus = 10
    option_yharon_dragon_of_rebirth = 11
    option_zenith = 12
    option_abominationn = 13
    option_calamity_final_bosses = 14
    option_primordial_wyrm = 15
    option_mutant = 16
    option_boss_rush = 17
    default = 0


class RandomizeNPCs(Toggle):
    """
    Randomizes all NPCs, putting them into the item pool. Fulfilling a certain NPC's recruit criteria rewards a check. :)
    """
    display_name = "Randomize NPCs"
    default = False


class EarlyAchievements(DefaultOnToggle):
    """Adds checks upon collecting early Pre-Hardmode achievements. Adds many sphere 1 checks."""

    display_name = "Early Pre-Hardmode Achievements"


class NormalAchievements(DefaultOnToggle):
    """
    Adds checks upon collecting achivements not covered by the other options. Achievements for
    clearing bosses and events are excluded.
    """

    display_name = "Normal Achievements"


class GrindyAchievements(Toggle):
    """Adds checks upon collecting grindy achievements"""

    display_name = "Grindy Achievements"


class FishingAchievements(Toggle):
    """Adds checks upon collecting fishing quest achievements"""

    display_name = "Fishing Quest Achievements"


class FillExtraChecksWith(Choice):
    """
    Applies if you have achievements enabled. "Useful Items" helps to make the early game less grindy.
    Items are rewarded to all players in your Terraria world.
    """

    display_name = "Fill Extra Checks With"
    option_coins = 0
    option_useful_items = 1
    default = 1
    
class CombatLogic(DefaultOnToggle):
    """
    Adds combat logic to prevent you fighting bosses the second they are technically available.
    Example is Old Duke is no longer in logic with just Post-Moon Lord.
    """
    
    display_name = "Combat Logic"

@dataclass
class TerrariaOptions(PerGameCommonOptions):
    calamity: Calamity
    fargo: Fargo
    getfixedboi: Getfixedboi
    goal: Goal
    randomize_npcs: RandomizeNPCs
    early_achievements: EarlyAchievements
    normal_achievements: NormalAchievements
    grindy_achievements: GrindyAchievements
    fishing_achievements: FishingAchievements
    fill_extra_checks_with: FillExtraChecksWith
    combat_logic: CombatLogic
    death_link: DeathLink