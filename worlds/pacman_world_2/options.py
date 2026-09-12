from Options import Choice, Range, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions
from dataclasses import dataclass


class TokenGoal(Range):
    """
    How many tokens should be required to goal.
    """
    
    display_name = "Token Goal"
    range_start = 0
    range_end = 152
    default = 0


class Tokensanity(DefaultOnToggle):
    """
    Tokens are now checks.
    """
    
    display_name = "Tokensanity"


class PacDotsanity(Range):
    """
    How many pac-dots will need to be collected to send a check.
    Setting it to 0 will disable Pac-Dots from being locations.
    """
    
    display_name = "PacDotsanity"
    range_start = 0
    range_end = 100


class LevelRando(Choice):
    """
    What type of levels should the randomizer shuffle
    """
    
    display_name = "Level Rando"
    option_disabled = 0
    option_levels = 1
    option_bosses = 2
    option_levels_and_bosses = 3


class SpookyRando(Toggle):
    """
    If bosses are included in the level shuffle, include Spooky.
    Your goal will be to beat the last level.
    This options does nothing if bosses are not in the shuffled levels.
    """
    
    display_name = "Include Spooky"


@dataclass
class PacManWorld2Options(PerGameCommonOptions):
    token_goal: TokenGoal
    tokensanity: Tokensanity
    pacdotsanity: PacDotsanity
    level_rando: LevelRando
    spooky_rando: SpookyRando
    death_link: DeathLink