from Options import Choice, Range, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions
from dataclasses import dataclass


class Goal(Choice):
    """
    Light World: Beat LW Dr. Fetus after collecting the 6 chapter keys
    Dark World: Beat DW Dr. Fetus after collecting the 6 chapter keys
    Light World Chapter 7: Beat all of Light World Chapter 7
    Dark World Chapter 7: Beat all of Dark World Chapter 7
    """

    display_name = "Goal"
    option_light_world = 0
    option_dark_world = 1
    option_light_world_chapter7 = 2
    option_dark_world_chapter7 = 3
    default = 0


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


class ChapterKeys(Toggle):
    """
    Enable this setting if you want chapter keys to be on bosses
    """
    
    display_name = "Chapter Keys On Bosses"


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
    If you start in Chapter 6, your character will be Super Meat Boy
    If you start in Chapter 7, your character will be Bandage Girl
    NOT YET IMPLEMENTED
    """

    display_name = "Starting Character"


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


@dataclass
class SMBOptions(PerGameCommonOptions):
    goal: Goal
    boss_req: BossReq
    lw_dr_fetus_req: LWDrFetusReq
    dw_dr_fetus_req: DWDrFetusReq
    chapter_keys: ChapterKeys
    bandages: Bandages
    dark_world: DarkWorld
    chapter_seven: ChapterSeven
    starting_chpt: StartingChpt
    # starting_char: StartingChar
    achievements: Achievements
    deathless_achievements: DeathlessAchievements
    speedrun_achievements: SpeedrunAchievements
    xmas: Xmas
    bandage_fill: BandageFill
    # death_link: DeathLink
    # death_link_amnesty: DeathLinkAmnesty