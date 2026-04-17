from Options import Choice, Range, OptionList, OptionSet, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions
from dataclasses import dataclass
from worlds.AutoWorld import World
from .locations import location_table
from .utils import get_achievements

class Goal(Choice):
    """
    Larries: Beat the Larries in Chapter 5
    Light World: Beat LW Dr. Fetus after collecting the 6 chapter keys
    Dark World: Beat DW Dr. Fetus after collecting the 6 chapter keys
    Light World Chapter 7: Beat all of Light World Chapter 7
    Dark World Chapter 7: Beat all of Dark World Chapter 7
    Boss Tokens: Collect all the boss tokens
    Bandage: McGuffin hunt to collect all the bandages
    Achievements: Obtain X amount of Achievement Tokens
    """

    display_name = "Goal"
    option_larries = 0
    option_light_world = 1
    option_dark_world = 2
    option_light_world_chapter7 = 3
    option_dark_world_chapter7 = 4
    option_boss_tokens = 5
    option_bandages = 6
    option_achievements = 7
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
    For every chapter you enable, the max amount will increase by 20 (expect for chapter 6, which increases by 5)
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
    Disable this setting if you need to collect all the chapter keys to reach your goal (this only applies if your goal is to beat lw/dw chapter 7).
    This setting will always be on if goal is boss tokens
    Another random chapter with a boss will be added if boss tokens is required but your only chapter is 5
    """
    
    display_name = "Boss Tokens"


class BossTokenReq(Range):
    """
    How many boss tokens require to goal
    """
    
    display_name = "Boss Token Requirement"
    range_start = 1
    range_end = 6
    default = 5


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


class Chapters(OptionSet):
    """
    Which chapters should be in the pool
    Enter any number between 1-7 for the respective chapter to be in the pool
    Enter "Random-X" with X being a number between 1-3 random chapter(s)
    Enter "Random-X+" with X being a number between 1-5 random chapter(s) with the inclusion of the last 2 chapters
    If you enter ["5", "Random-4+"] then chapter 5 and 4 other random chapters will be selected.
    If any of the last 3 chapters aren't in the pool, your goal will be boss tokens.
    If you only have one chapter enabled and its either of the last 2 chapters, then one random chapter between 1-5 will be added.
    """
    
    display_name = "Chapters"
    valid_keys = {
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "Random-1",
        "Random-2",
        "Random-3",
        "Random-1+",
        "Random-2+",
        "Random-3+",
        "Random-4+",
        "Random-5+"
        }
    default = ["1", "2", "3", "4", "5", "6"]


class StartingChpt(Range):
    """
    Choose Starting Chapter
    If your starting chapter isn't in the list of chapters, a random one from that list will be picked.
    """

    display_name = "Starting Chapter"
    range_start = 1
    range_end = 6
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
    option_brownie = 14
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

# +2 xmas
class AchievementTokens(Range):
    """
    Tokens needed to reach goal. Max varies by settings:
    Normal: 2 base, 2 per chpt 1-6 (12 total), +1 with any chpt 1-5, +1 chpt 7, +2 DW, +1 DW + chpt 6, +1 DW + chpt 7, +3 bandages, +3 bandages + DW
    Speedrun: 1 per chpt 1-5 (5 total)
    Deathless: 1 per chpt 1-7 (7 total, 14 total with DW)
    """
    
    display_name = "Achievement Tokens"
    range_start = 1
    range_end = 45
    default = 18

class Xmas(Toggle):
    """
    Puts all the xmas levels into the pool (and achievements if normal achievements are in the pool)
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
    How many deaths should it take to send a DeathLink
    """

    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 20
    default = 10


def resolve_options(world: World):
    # Add chapters, add random amount based on available left
    # First add 1 random chapter if you only have either of the last 2 chapters enabled
    if world.options.chapters.value.issubset({"6", "7"}):
        available_low = {"1", "2", "3", "4", "5"} - world.options.chapters.value
        if available_low:
            world.options.chapters.value.add(world.multiworld.random.choice(list(available_low)))
    
    all_chpts = {str(i) for i in range(1, 8)}

    selected_chpts = set()
    random_entries = []

    # Split fixed and random
    for chpt in world.options.chapters.value:
        if chpt.startswith("Random"):
            random_entries.append(chpt)
        else:
            selected_chpts.add(chpt)

    # Available pool
    available_chpts = all_chpts - selected_chpts

    # Handle Random-X entries
    for entry in random_entries:
        amount_part = entry.split('-', 1)[1]
        has_plus = amount_part.endswith('+')
        amount = int(amount_part.rstrip('+'))

        pool = available_chpts.copy()
        if not has_plus:
            pool -= {"6", "7"}

        if amount > len(pool):
            amount = len(pool)

        picks = set(world.multiworld.random.sample(list(pool), amount))

        selected_chpts |= picks
        available_chpts -= picks
        
        if selected_chpts.issubset({"6", "7"}):
            extra_pool = all_chpts - selected_chpts

            if extra_pool:
                selected_chpts.add(world.multiworld.random.choice(list(extra_pool)))


    world.options.chapters.value = selected_chpts

    # If goal requires a specific chapter that's not enabled, default to boss tokens
    if world.options.goal == "larries" and "5" not in world.options.chapters.value:
        world.options.goal.value = 5
    elif world.options.goal in ("light_world", "dark_world") and "6" not in world.options.chapters.value:
        world.options.goal.value = 5
    elif world.options.goal in ("light_world_chapter7", "dark_world_chapter7") and "7" not in world.options.chapters.value:
        world.options.goal.value = 5
    
    # If goal is boss tokens, force enable boss tokens
    if world.options.goal == "boss_tokens":
        world.options.boss_tokens.value = Toggle.option_true
        
        # make sure there are at least 2 chapters if your only chapter is 5
        if world.options.chapters.value == {"5"}:
            while len(world.options.chapters.value) < 2:
                world.options.chapters.value.add(str(world.multiworld.random.randint(1, 6)))
        
    # cap boss tokens
    boss_token_max: int = 0
    bosses = ["1", "2", "3", "4"]
    
    if world.options.goal != "larries":
        bosses.append("5")
    if world.options.goal != "light_world":
        bosses.append("6")
    if world.options.goal != "dark_world" and world.options.dark_world.value:
        bosses.append("6")
        
    for chpt in bosses:
        if chpt in world.options.chapters.value:
            boss_token_max += 1

    world.options.boss_token_req.value = min(world.options.boss_token_req.value, boss_token_max)
    
    # Ensure starting_chpt is in the enabled chapters
    if str(world.options.starting_chpt.value) not in world.options.chapters.value:
        world.options.starting_chpt.value = int(world.multiworld.random.choice(list(world.options.chapters.value)))
        
    # Force dark world levels enabled if our goal is in dark world
    if world.options.goal in ("dark_world", "dark_world_chapter7"):
        world.options.dark_world.value = Toggle.option_true
        
    # Set bandage fill to 0 if our goal isn't bandages
    if world.options.goal != "bandages":
        world.options.bandage_fill.value = 0
        
    # Cap DW Dr. Fetus Keys Amount
    dr_fetus_cap: int = 0
    for chpt in world.options.chapters.value:
        if chpt == "6":
            dr_fetus_cap += 5
        else:
            dr_fetus_cap += 20
    
    world.options.dw_dr_fetus_req.value = min(world.options.dw_dr_fetus_req.value, dr_fetus_cap)
        
    # Cap Bandages
    # if world.options.goal == "bandages" and not world.options.dark_world.value:
    #     world.options.bandages_amount.value = min(world.options.bandages_amount.value, 52)
    if world.options.goal == "bandages":
        bandages_cap: int = 0
        
        for i in range(1, 6):
            if str(i) in world.options.chapters.value:
                if i == 3:
                    bandages_cap += 8
                    bandages_cap += world.options.dark_world.value * 12
                else:
                    bandages_cap += 11
                    bandages_cap += world.options.dark_world.value * 9
        
        world.options.bandages_amount.value = min(world.options.bandages_amount.value, bandages_cap)

    # If starting chapter is 7 but our goal is to complete all of lw/dw chapter 7, select a random chapter
    if world.options.starting_chpt.value == 7 and world.options.goal in ("light_world_chapter7", "dark_world_chapter7"):
        while world.options.starting_chpt.value == 7:
            world.options.starting_chpt.value = int(world.multiworld.random.choice(list(world.options.chapters.value)))
        
    # If our goal is achievements and none of the achievement goals are on, put normal in.
    if world.options.goal == "achievements" and not world.options.achievement_goals.value:
        world.options.achievement_goals.value.append("normal")
        
    # If our goal is achievements and normal is enabled, enable normal achievements
    if world.options.goal == "achievements" and "normal" in world.options.achievement_goals.value:
        world.options.achievements.value = Toggle.option_true
        
    # If our goal is achievements and deathless is enabled, enable deathless achievements
    if world.options.goal == "achievements" and "deathless" in world.options.achievement_goals.value:
        world.options.deathless_achievements.value = Toggle.option_true
    
    # If our goal is achievements and speedrun is enabled, enable speedrun achievements
    if world.options.goal == "achievements" and "speedrun" in world.options.achievement_goals.value:
        world.options.speedrun_achievements.value = Toggle.option_true
        
    # If speedrun achievements are enabled, enable dark world levels
    if world.options.speedrun_achievements.value:
        world.options.dark_world.value = Toggle.option_true
        
    # Cap Achievement Token amount if our goal is achievements
    if world.options.goal == "achievements":
        locs = len(get_achievements(world.options, location_table))
        world.options.achievement_tokens.value = min(world.options.achievement_tokens.value, locs)

@dataclass
class SMBOptions(PerGameCommonOptions):
    goal: Goal
    boss_req: BossReq
    lw_dr_fetus_req: LWDrFetusReq
    dw_dr_fetus_req: DWDrFetusReq
    bandages_amount: BandagesAmount
    boss_tokens: BossTokens
    boss_token_req: BossTokenReq
    bandages: Bandages
    dark_world: DarkWorld
    chapters: Chapters
    starting_chpt: StartingChpt
    starting_char: StartingChar
    achievements: Achievements
    deathless_achievements: DeathlessAchievements
    speedrun_achievements: SpeedrunAchievements
    achievement_goals: AchievementGoals
    achievement_tokens: AchievementTokens
    # xmas: Xmas
    bandage_fill: BandageFill
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty