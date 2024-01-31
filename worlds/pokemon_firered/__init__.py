import settings
from typing import ClassVar

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .rom import PokemonFireRedDeltaPatch


class PokemonFireRedSettings(settings.Group):
    class PokemonFireRedRomFile(settings.UserFilePath):
        """File name of your English Pokemon FireRed ROM"""
        description = "Pokemon FireRed ROM File"
        copy_to = "Pokemon - FireRed Version (USA, Europe) (Rev 1).gba"
        md5 = [PokemonFireRedDeltaPatch.hash]

    rom_file: PokemonFireRedRomFile = PokemonFireRedRomFile(
        PokemonFireRedRomFile.copy_to)


class PokemonFireRedWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon FireRed with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["Zuils"]
    )

    tutorials = [setup_en]


class PokemonFireRedWorld(World):
    """
    Pokemon FireRed is a beloved remake of the Kanto region of Pokemon.
    """
    game = "Pokemon FireRed"
    web = PokemonFireRedWebWorld()
    topology_present = True

    settings_key = "pokemon_firered_settings"
    settings: ClassVar[PokemonFireRedSettings]
