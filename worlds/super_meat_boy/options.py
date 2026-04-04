from Options import Choice, Range, OptionList, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions
from dataclasses import dataclass
from worlds.AutoWorld import World


class Goal(Choice):
    """
    Larries: Beat the Larries in Chapter 5
    Light World: Beat LW Dr. Fetus after collecting the 6 chapter keys
    Dark World: Beat DW Dr. Fetus after collecting the 6 chapter keys
    Light World Chapter 7: Beat all of Light World Chapter 7
    Dark World Chapter 7: Beat all of Dark World Chapter 7
    Bandage: McGuffin hunt to collect all the bandages
    Achievements: Obtain X amount of Achievement Tokens
    """

    display_name = "Goal"
    option_larries = 0
    option_light_world = 1
    option_dark_world = 2
    option_light_world_chapter7 = 3
    option_dark_world_chapter7 = 4
    option_bandages = 5
    option_achievements = 6
    default = 1


class BossReq(Range):
    """
    How many boss keys are required to fight the boss (only affects Chapters 1-5)
    """

    display_name = "Boss Requirement"
    range_start = 0
    range_end = 20
    default = 17


class LWDrFetusReq(Range):
    """
    How many boss keys are required to fight LW Dr. Fetus
    """
    display_name = "LW Dr. Fetus Requirement"
    range_start = 0
    range_end = 5
    default = 5


class DWDrFetusReq(Range):
    """
    How many DW Dr. Fetus Keys should be required to fight DW Dr. Fetus
    This setting does nothing if you do not have dark world levels enabled
    If you don't have chapter 7 levels enabled, the max is 105
    """

    display_name = "DW Dr. Fetus Requirement"
    range_start = 0
    range_end = 125
    default = 85


class BandagesAmount(Range):
    """
    If your goal is bandages, how many are required to goal
    If there are no dark world levels, the max amount is 52.
    """
    display_name = "Bandages Amount"
    range_start = 1
    range_end = 100
    default = 100


class BossTokens(Toggle):
    """
    Enable this setting if you want to put boss tokens on all the bosses to require to goal
    Disable this setting if you need to collect all the chapter keys to reach your goal.
    The above statement only applies if you need to beat lw/dw chapter 7
    """
    
    display_name = "Boss Tokens"


class Bandages(Toggle):
    """
    Enables the bandage collectibles as locations.
    """

    display_name = "Bandages"


class DarkWorld(DefaultOnToggle):
    """
    If the goal is LW Dr. Fetus or LW Chapter 7, enable dark world levels
    This setting will always be on if your setting is DW Dr. Fetus or DW Chapter 7
    """

    display_name = "Enable Dark World Levels"


class ChapterSix(DefaultOnToggle):
    """
    Enables Chapter 6 levels
    This setting will be always on if your goal is LW/DW Dr. Fetus
    """
    display_name = "Enable Chapter 6 Levels"


class ChapterSeven(Toggle):
    """
    Enables Chapter 7 levels
    This setting will always be on if your goal is LW/DW Chapter 7
    """

    display_name = "Enable Chapter 7 Levels"


class StartingChpt(Range):
    """
    Choose Starting Chapter
    """

    display_name = "Starting Chapter"
    range_start = 1
    range_end = 7
    default = 1


class StartingChar(Choice):
    """
    Choose Starting Character
    If you start in Chapter 6, your character will be Meat Boy
    If you start in Chapter 7, your character will be Bandage Girl
    """

    display_name = "Starting Character"
    option_meat_boy = 0
    option_8bit_meat_boy = 1
    option_4bit_meat_boy = 2
    option_4color_meat_boy = 3
    option_commander_video = 4
    option_jill = 5
    option_ogmo = 6
    option_flywrench = 7
    option_the_kid = 8
    option_josef = 9
    option_naija = 10
    option_runman = 11
    option_steve = 12
    option_meat_ninja = 13
    default = 0


class Achievements(Toggle):
    """
    Puts most steam achievements in the pool
    """

    display_name = "Achievements"


class DeathlessAchievements(Toggle):
    """
    Puts all deathless achievements in the pool
    """

    display_name = "Deathless Achievements"


class SpeedrunAchievements(Toggle):
    """
    Puts all speedrun achievements in the pool
    Dark world levels will automatically be enabled if this is turned on.
    """

    display_name = "Speedrun Achievements"


class AchievementGoals(OptionList):
    """
    Which achievements should count towards the goal.
    If none are present, the normal achievements will be on.
    Valid options are "normal", "deathless", "speedrun"
    Achievements will be automatically turned on if they are present in this option
    This setting does nothing if your goal is NOT achievements.
    """
    
    display_name = "Achievement Goals"
    valid_keys = {"normal", "deathless", "speedrun"}
    default = ["normal"]


class AchievementTokens(Range):
    """
    How many achievement tokens do you need to reach your goal.
    Depending on what settings you have the max amount will change:
    13 with normal enabled
    2 with normal and chapter 6 enabled
    1 with normal and chapter 7 enabled
    3 with normal and bandages enabled
    2 with normal and dark world enabled
    1 with normal, chapter 6, and dark world enabled
    1 with normal, chapter 7, and dark world enabled
    3 with normal, bandages, and dark world enabled
    2 with normal and xmas enabled
    5 with speedrun and dark world enabled
    5 with deathless enabled
    1 with deathless and chapter 6 enabled
    1 with deathless and chapter 7 enabled
    5 with deathless and dark world enabled
    1 with deathless, dark world, and chapter 6 enabled
    1 with deathless, dark world, and chapter 7 enabled
    """
    
    display_name = "Achievement Tokens"
    range_start = 1
    range_end = 47
    default = 18

class Xmas(Toggle):
    """
    Puts all the xmas levels into the pool
    DO NOT ENABLE THIS SETTING IT IS NOT IMPLEMENTED
    """

    display_name = "Xmas"
    

class BandageFill(Range):
    """
    What percentage of the multiworld should the remaining items be bandages.
    This setting only works if your goal is bandages
    """
    display_name = "Bandage Fill"
    range_start = 0
    range_end = 100
    default = 50


class DeathLinkAmnesty(Range):
    """
    How many death links should it take to send a DeathLink
    DEATHLINK IS NOT YET IMPLEMENTED
    """

    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 20
    default = 10


def resolve_options(world: World):
    # Force chapter 7 levels to be on if our goal is in chapter 7 or if our starting chapter is 7
    if world.options.goal in ("light_world_chapter7", "dark_world_chapter7") or world.options.starting_chpt.value == 7:
        world.options.chapter_seven.value = 1
    
    # Force chapter 6 levels to be on if starting chapter is 6 or our goal is either light world or dark world
    if world.options.starting_chpt.value == 6 or world.options.goal in ("light_world", "dark_world"):
        world.options.chapter_six.value = 1
        
    # Force dark world levels enabled if our goal is in dark world
    if world.options.goal in ("dark_world", "dark_world_chapter7"):
        world.options.dark_world.value = 1
        
    # Set bandage fill to 0 if our goal isn't bandages
    if world.options.goal != "bandages":
        world.options.bandage_fill.value = 0
        
    # Cap DW Dr. Fetus Keys Amount if we don't have chapter 7 levels enabled
    if not world.options.chapter_seven.value:
        world.options.dw_dr_fetus_req.value = min(world.options.dw_dr_fetus_req.value, 105)
        
    # Cap Bandages if dark world levels aren't enabled
    if world.options.goal == "bandages" and not world.options.dark_world.value:
        world.options.bandages_amount.value = min(world.options.bandages_amount.value, 52)

    # If starting chapter is 7 but our goal is to complete all of lw/dw chapter 7, select a random chapter
    if (world.options.starting_chpt.value == 7 and world.options.goal in ("light_world_chapter7", "dark_world_chapter7")):
        world.options.starting_chpt.value = world.multiworld.random.randint(1, 7 if world.options.chapter_six.value else 6)
        
    # If our goal is achievements and none of the achievement goals are on, put normal in.
    if world.options.goal == "achievements" and not world.options.achievement_goals.value:
        world.options.achievement_goals.value.append("normal")
        
    # If our goal is achievements and normal is enabled, enable normal achievements
    if world.options.goal == "achievements" and "normal" in world.options.achievement_goals.value:
        world.options.achievements.value = 1
        
    # If our goal is achievements and deathless is enabled, enable deathless achievements
    if world.options.goal == "achievements" and "deathless" in world.options.achievement_goals.value:
        world.options.deathless_achievements.value = 1
    
    # If our goal is achievements and speedrun is enabled, enable speedrun achievements
    if world.options.goal == "achievements" and "speedrun" in world.options.achievement_goals.value:
        world.options.speedrun_achievements.value = 1
        
    # If speedrun achievements are enabled, enable dark world levels
    if world.options.speedrun_achievements.value:
        world.options.dark_world.value = 1
        
    # Cap Achievement Token amount if our goal is achievements
    if world.options.goal == "achievements":
        max_amount: int = 0
        
        if "normal" in world.options.achievement_goals.value:
            max_amount += 13
            if world.options.chapter_six.value:
                max_amount += 2
            if world.options.chapter_seven.value:
                max_amount += 1
            if world.options.bandages.value:
                max_amount += 3
            if world.options.dark_world.value:
                max_amount += 2
            if world.options.chapter_six.value and world.options.dark_world.value:
                max_amount += 1
            if world.options.chapter_seven.value and world.options.dark_world.value:
                max_amount += 1
            if world.options.bandages.value and world.options.dark_world.value:
                max_amount += 3
            if world.options.xmas.value:
                max_amount += 2

        if "speedrun" in world.options.achievement_goals.value and world.options.dark_world.value:
            max_amount += 5

        if "deathless" in world.options.achievement_goals.value:
            max_amount += 5
            if world.options.chapter_six.value:
                max_amount += 1
            if world.options.chapter_seven.value:
                max_amount += 1
            if world.options.dark_world.value:
                max_amount += 5
            if world.options.chapter_six.value and world.options.dark_world.value:
                max_amount += 1
            if world.options.chapter_seven.value and world.options.dark_world.value:
                max_amount += 1

        world.options.achievement_tokens.value = min(world.options.achievement_tokens.value, max_amount)

@dataclass
class SMBOptions(PerGameCommonOptions):
    goal: Goal
    boss_req: BossReq
    lw_dr_fetus_req: LWDrFetusReq
    dw_dr_fetus_req: DWDrFetusReq
    bandages_amount: BandagesAmount
    boss_tokens: BossTokens
    bandages: Bandages
    dark_world: DarkWorld
    chapter_six: ChapterSix
    chapter_seven: ChapterSeven
    starting_chpt: StartingChpt
    starting_char: StartingChar
    achievements: Achievements
    deathless_achievements: DeathlessAchievements
    speedrun_achievements: SpeedrunAchievements
    achievement_goals: AchievementGoals
    achievement_tokens: AchievementTokens
    xmas: Xmas
    bandage_fill: BandageFill
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty