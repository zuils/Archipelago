from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions, Toggle, DefaultOnToggle, Range, OptionSet, OptionGroup


class Mods(OptionSet):
    """
    Which content mods to be played with.
    Valid options are Calamity and Fargo.
    If both are enabled, it is expected to be played with the Fargo's Souls DLC Mod.
    """
    display_name = "Mods"
    valid_keys = {
        "Calamity",
        "Fargo"
    }

class Getfixedboi(Toggle):
    """
    Generation accomodates the secret, very difficult "getfixedboi" seed

    FOR THE BETA: Getfixedboi is not compatible with the following settings:
    - Princess goal enabled
    - NPC Rando enabled
    - Fargo's Souls enabled
    If any of these apply, Getfixedboi will automatically be disabled during generation.
    """

    display_name = "getfixedboi Seed"


class Goal(Choice):
    """
    The victory condition for your run. Stuff after the goal will not be shuffled (if Shuffle Up To is default).
    Primordial Wyrm and Boss Rush are accessible relatively early, so consider "Items" or
    "Locations" accessibility to avoid getting stuck on the goal.

    FOR THE BETA: Note that the Wall of Flesh goal is intended to be played with NPC Rando on.
    Otherwise, the generated game will be immediately goal-able.
    Deviantt goal can be goaled in sphere 1, it is intended to be played in very short syncs.
    """

    display_name = "Goal"
    option_deviantt = 0
    option_wall_of_flesh = 1
    option_mechanical_bosses = 2
    option_calamitas_clone = 3
    option_plantera = 4
    option_princess = 5
    option_golem = 6
    option_empress_of_light = 7
    option_lunatic_cultist = 8
    option_astrum_deus = 9
    option_moon_lord = 10
    option_providence_the_profaned_goddess = 11
    option_devourer_of_gods = 12
    option_eridanus_champion_of_cosmos = 13
    option_yharon_dragon_of_rebirth = 14
    option_zenith = 15
    option_abominationn = 16
    option_calamity_final_bosses = 17
    option_primordial_wyrm = 18
    option_mutant = 19
    option_boss_rush = 20
    option_soul_of_eternity = 21
    default = 1


class ShuffleUpTo(Choice):
    """
    Allows you to randomize checks past the set goal.
    Note that certain configurations may result in some checks only being accessible post-goal.
    """
    display_name = "Shuffle Up To"
    default = 0
    option_disable = 0
    option_mechanical_bosses = 2
    option_plantera = 4
    option_golem = 6
    option_lunatic_cultist = 8
    option_moon_lord = 10
    option_providence_the_profaned_goddess = 11
    option_devourer_of_gods = 12
    option_eridanus_champion_of_cosmos = 13
    option_yharon_dragon_of_rebirth = 14
    option_abominationn = 16
    option_calamity_final_bosses = 17
    option_mutant = 19
    option_all = -1

class RandomizeNPCs(DefaultOnToggle):
    """
    Randomizes all vanilla NPCs, putting them into the item pool. Fulfilling a certain NPC's recruit criteria rewards a check.
    """
    display_name = "Randomize NPCs"


class RandomizeDepth(Choice):
    """
    Randomizes the maximum depth you are able to traverse, initially restricting you to the Surface and Space layers.
    Receiving "Progressive Depth" items increments how many layers you can traverse downward, through the Underground, Cavern and Underworld respectively.
    Adds checks upon collecting the achievements "Into Orbit", "It's Getting Hot in Here" and "Rock Bottom".

    Use the gen safety option if you want structures and items that vary in spawn depth to require their deepest
    possible layer to be accessible.
    If you plan on playing on a small world, consider enabling gen_safety_small.
    """

    display_name = "Randomize Maximum Depth"
    option_off = 0
    option_on = 1
    option_gen_safety = 2
    option_gen_safety_small = 3
    default = 0


class EarlyAchievements(DefaultOnToggle):
    """Adds checks upon collecting early Pre-Hardmode achievements. Adds many sphere 1 checks."""

    display_name = "Early Pre-Hardmode Achievements"


class NormalAchievements(DefaultOnToggle):
    """
    Adds checks upon collecting achievements not covered by the other options. Achievements for
    clearing bosses and events are excluded.
    """

    display_name = "Normal Achievements"


class RareAchievements(Toggle):
    """Adds checks upon collecting grindy achievements involving rare enemies/drops"""

    display_name = "Rare Achievements"


class TimeAchievements(Toggle):
    """
    Adds checks upon collecting grindy achievements based on random time-based events, such as windy weather
    """

    display_name = "Time-based Achievements"


class CraftingAchievements(Toggle):
    """Adds checks upon collecting grindy achievements dedicated to crafting complex items"""

    display_name = "Crafting Achievements"


class GrindyAchievements(Toggle):
    """Adds checks upon collecting grindy achievements that otherwise require a lot of repetitive work"""

    display_name = "Grindy Achievements"


class FishingAchievements(Toggle):
    """
    Adds checks upon collecting fishing quest achievements.
    If enabled, will also enable fishing logic.
    """

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


class FishingSkips(Toggle):
    """
    Enables sequence breaks in logic requiring the use of fishing or angler quests for items.
    If disabled, certain achievements (like Black Mirror) may become inaccessible.
    """

    display_name = "Fishing Skips"



class ShimmerSkips(Toggle):
    """
    Enables sequence breaks in logic requiring the use of Shimmer to transmute/uncraft items.
    """

    display_name = "Shimmer Skips"


class CombatLogic(Choice):
    """
    Guarantees you will not have to fight a boss/event without access to prior health upgrades/gear.
    Setting it to health logic will only put bosses in logic based on what health upgrades you can get (mainly alters Calamity logic)
    Setting it to gear logic will only put bosses in logic based on what gear is obtainable (alters vanilla, calamity, and fargo logic)
    Keeping this setting off will expect you to fight bosses with gear that is not viable.
    
    I hope you like reading :) Here is gear logic (if you do not recognize the name of these items assume its calamity mod):
    Trojan Squirrel to Calamity Evil Bosses - underground (if depth rando enabled)
    Queen Bee to WoF - cavern (if depth rando enabled)
    queen slime to skele prime - underground (if depth rando enabled) and cobalt/mythril/adamantite/forbidden/crystal assassin/spider/titan heart and any wings/bundle of balloons
    cal clone to duke fishron - adamantite/chlorophyte/hallowed/turtle/reaver/shroomite/brimflame/spectre/tiki/fathom swarmer/umbraphile/daedalus and any wings/bundle of balloons
    plaguebringer to dragonfolly - beetle/hydrothermic/reaver/shroomite/plague reaper/lunic corps/astral/plaguebringer/gaia (if fargo enabled) and betsy/empress/fishron wings
    profaned guardians to polterghast - lunar armor/tarragon/prismatic and celestial starboard/lunar wings/moon walkers/tarragon wings
    dog and yharon - bloodflare/omega blue/prismatic and dash shield or statis ninja belt and elysian/tarragon wings/moon walkers
    final bosses and eidolyn wyrm - god slayer/silva/auric tesla and wings of rebirth/void strikers and dash shield or statis ninja belt
    boss rush - auric tesla/demonshade/gem tech and wings of rebirth/seraph tracers and dash shield or statis ninja void belt

    fargo:
    for the champions: gaia/stardust/god slayer or silva (if calamity is enabled), flight mastery soul (if calamity disabled) or force of the gale or elysian/tarragon wings/moon walkers (if calamity is enabled), 2 forces, 1 damage soul (if calamity disabled)
    abominationn: eridanus armor/auric tesla (if calamity is enabled), flight mastery soul/force of the gale (if calamity is enabled), 3 forces, 1 damage soul (if calamity disabled)
    mutant: styx armor/auric tesla (if calamity is enabled), soul of terraria, soul of dimensions & universe
    """
    
    display_name = "Combat Logic"
    option_none = 0
    option_health = 1
    option_gear = 2
    option_both = 3
    default = 2


class HealthLogicHandicap(Range):
    """
    If health logic is on, this option allows you to reduce how many types of health consumables are needed before a boss.
    For example, if set to 0, Moon Lord will require Life Crystals/Fruits, Sanguine Tangerine, and Miracle Fruit.
    If set to -1, you only need Sanguine Tangerine or Miracle Fruit. If set to -2, neither are required.
    """
    
    display_name = "Health Handicap"
    range_start = -6
    range_end = 0
    default = 0


class GearLogicHandicap(Range):
    """
    If gear logic is on, this option will adjust the requirements for each boss.
    For example, if set to 1, instead of Skeletron requiring you to have the cavern layer unlocked, it'll expect you to beat him with only the underground layer.
    If set to 2, Queen Slime would expect you to beat her with only underground layer instead of having early hardmode equipment.
    
    This handicap won't apply to the first bosses. So Trojan Squirrel will still require Underground (if depth rando is enabled) if this setting is higher than 1.
    """
    
    display_name = "Gear Handicap"
    range_start = 0
    range_end = 3
    default = 0


class CompressedPlaythrough(DefaultOnToggle):
    """
    Turn this on if you want the playthrough in the spoiler log to be compressed so it only shows the locations.
    Turn this off if you want the playthrough in the spoiler log to show both locations and events. 
    """

    display_name = "Compressed Playthrough"


ter_option_groups = [
    OptionGroup("Gamemode and Content", [
        Mods,
        Getfixedboi,
        Goal,
        ShuffleUpTo,
    ]),
    OptionGroup("Checks", [
        RandomizeNPCs,
        RandomizeDepth,
        EarlyAchievements,
        NormalAchievements,
        RareAchievements,
        TimeAchievements,
        CraftingAchievements,
        GrindyAchievements,
        FishingAchievements,
    ]),
    OptionGroup("Items", [
        FillExtraChecksWith,
    ]),
    OptionGroup("Logic", [
        FishingSkips,
        ShimmerSkips,
        CombatLogic,
        HealthLogicHandicap,
        GearLogicHandicap,
    ]),
]

@dataclass
class TerrariaOptions(PerGameCommonOptions):
    mods: Mods
    getfixedboi: Getfixedboi
    goal: Goal
    shuffle_to: ShuffleUpTo
    randomize_npcs: RandomizeNPCs
    randomize_depth: RandomizeDepth
    early_achievements: EarlyAchievements
    normal_achievements: NormalAchievements
    rare_achievements: RareAchievements
    time_achievements: TimeAchievements
    crafting_achievements: CraftingAchievements
    grindy_achievements: GrindyAchievements
    fishing_achievements: FishingAchievements
    fill_extra_checks_with: FillExtraChecksWith
    fishing_skips: FishingSkips
    shimmer_skips: ShimmerSkips
    combat_logic: CombatLogic
    health_logic_handicap: HealthLogicHandicap
    gear_logic_handicap: GearLogicHandicap
    compressed_playthrough: CompressedPlaythrough
    death_link: DeathLink
