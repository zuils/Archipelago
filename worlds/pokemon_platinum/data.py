"""
Pulls data from JSON files in worlds/pokemon_emerald/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location labels or usable pokemon species), some cleanup
and sorting, and Warp methods.
"""
from dataclasses import dataclass
import copy
from enum import IntEnum
import orjson
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Tuple, Any, Union
import pkgutil
import pkg_resources

from BaseClasses import ItemClassification

SAVE_FILE_OFFSET = 0x27E000
FLAGS_OFFSET = 0xFEC
PKTCH_OFFSET = 0x1163
BASE_OFFSET = 0x38C750

class SpeciesData:
    name: str
    species: int
    abilities: Tuple[int, int, int]
    types: Tuple[str, str]
    catchrate: int
    learn_moves: List[Tuple[int, int]]


class PokemonPlatinumData:
    starters: Tuple[int, int, int]
    constants: Dict[str, int]
    ram_addresses: Dict[str, int]
    rom_addresses: Dict[str, int]
    #
    #regions: Dict[str, RegionData]
    #locations: Dict[str, LocationData]
    #items: Dict[int, ItemData]
    #species: List[Optional[SpeciesData]]
    #static_encounters: List[StaticEncounterData]
    #tmhm_moves: List[int]
    #abilities: List[AbilityData]
    #maps: List[MapData]
    #warps: Dict[str, Warp]
    #warp_map: Dict[str, Optional[str]]
    #trainers: List[TrainerData]

    def __init__(self) -> None:
        self.starters = (387, 390, 393)
        self.constants = {}
        self.ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.items = {}
        self.species = []
        self.static_encounters = []
        self.tmhm_moves = []
        self.abilities = []
        self.maps = []
        self.warps = {}
        self.warp_map = {}
        self.trainers = []


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode('utf-8-sig'))


data = PokemonPlatinumData()


def create_data_copy() -> PokemonPlatinumData:
    new_copy = PokemonPlatinumData()
    new_copy.species = copy.deepcopy(data.species)
    new_copy.tmhm_moves = copy.deepcopy(data.tmhm_moves)
    new_copy.maps = copy.deepcopy(data.maps)
    new_copy.static_encounters = copy.deepcopy(data.static_encounters)
    new_copy.trainers = copy.deepcopy(data.trainers)


def _init() -> None:
    print('unimplemented')



_init()
