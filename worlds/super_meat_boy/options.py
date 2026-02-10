from Options import Choice, Range, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions
from dataclasses import dataclass


class Goal(Choice):
    """
    Larries: Beat the Larries in Chapter 5
    Light World: Beat LW Dr. Fetus after collecting the 6 chapter keys
    Dark World: Beat DW Dr. Fetus after collecting the 6 chapter keys
    Light World Chapter 7: Beat all of Light World Chapter 7
    Dark World Chapter 7: Beat all of Dark World Chapter 7
    Bandage: McGuffin hunt to collect all the bandages
    """

    display_name = "Goal"
    option_larries = 0
    option_light_world = 1
    option_dark_world = 2
    option_light_world_chapter7 = 3
    option_dark_world_chapter7 = 4
    option_bandages = 5
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
    If you don't have chapter 6 levels enabled, the max is 100
    """

    display_name = "DW Dr. Fetus Requirement"
    range_start = 0
    range_end = 125
    default = 85


class BandagesAmount(Range):
    """
    If your goal is bandages, how many are required to goal
    If there are dark world levels, there are 100 in the pool
    If there are no dark world levels, there are 52 in the pool
    """
    display_name = "Bandages Amount"
    range_start = 1
    range_end = 100
    default = 100


class BossTokens(Toggle):
    """
    Enable this setting if you want to put boss tokens on all the bosses to require to goal
    Disable this setting if you need to collect all the chapter keys to reach your goal (this only applies if you need to beat lw/dw chapter 7)
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
    This setting will be always on if your goal is NOT to beat larries or bandages
    Chapter 7 levels will automatically be disabled if this is off
    """
    display_name = "Enable Chapter 6 Levels"


class ChapterSeven(Toggle):
    """
    Enables Chapter 7 levels
    This setting will always be on if your goal is to complete either LW or DW Chapter 7
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
    Choose Starting Chapter
    If you start in Chapter 6, your character will be Meat Boy
    If you start in Chapter 7, your character will be Bandage Girl
    """

    display_name = "Starting Character"
    option_meat_boy = 0
    option_8_bit_meat_boy = 1
    option_4_bit_meat_boy = 2
    option_4_color_meat_boy = 3
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
    This setting will always be off if there are no dark world levels in the pool
    """

    display_name = "Speedrun Achievements"


class Xmas(Toggle):
    """
    Puts all the xmas levels into the pool
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
    NOT YET IMPLEMENTED
    """

    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 20
    default = 10


class Debug(Toggle):
    """
    Gives you every A+ Rank at the start
    """


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
    xmas: Xmas
    bandage_fill: BandageFill
    # death_link: DeathLink
    # death_link_amnesty: DeathLinkAmnesty
    debug: Debug