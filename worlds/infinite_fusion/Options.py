from typing import Dict
from Options import Choice, Range, Option, Toggle, DefaultOnToggle, OptionSet


class Badgesanity(Toggle):
    """
    Puts all badges into the pool
    """
    display_name = "Enable Badgesanity"


class Johto(Toggle):
    """
    Enables Johto
    """
    display_name = "Enable Johto"


class Sevii(Toggle):
    """
    Enables Sevii Islands
    """
    display_name = "Enable Sevii Islands"


'''
class StartingRegion(Choice):
    """
    Choose Starting Region
    """
    display_name = "Starting Region"
    option_kanto = 0
    option_johto = 1
    option_random = 2
    default = 0
'''

infinitefusion_options: Dict[str, Option] = {
    "badgesanity": Badgesanity,
    "johto": Johto,
    "sevii": Sevii
    # "starting_region": StartingRegion
}
