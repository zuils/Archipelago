"""
Pulls data from JSON files in worlds/pokemon_emerald/data/ into classes.
This also includes marrying automatically extracted data with manually
defined data (like location labels or usable pokemon species), some cleanup
and sorting, and Warp methods.
"""
import copy
import orjson
from typing import Dict, List, NamedTuple, Optional, Set, FrozenSet, Tuple, Any, Union
import pkgutil
from .structs import ItemEntry, LocationEntry, TriggerEntry, TrainerEntry

from BaseClasses import ItemClassification

FLAGS_OFFSET = 0xFEC
PKTCH_OFFSET = 0x1163

# These are all to data 001, not 000
# Trainer Pokemon Data
TRPOKE_DATA_OFFSET = 0x372633C
# Trainer Data
TRDATA_DATA_OFFSET = 0x371FD48
# Map Event Data (needed to change what items are given)
EVENT_DATA_OFFSET = 0x471C2F4


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
    locations: Dict[LocationEntry]
    items: Dict[ItemEntry]
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
        #self.warps = {}
        #self.warp_map = {}
        self.trainers = []

        self.rom_addresses["globalPtr"] = 0xBA8
        # Set on game load
        self.rom_addresses["versionPtr"] = 0x0
        self.rom_addresses["savefileBase"] = 0x0


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
    return new_copy


def _init() -> None:
    data.items = load_json_data("items.json")
    data.items.append(load_json_data("hidden_items.json"))
    data.locations = load_json_data("locations.json")
    data.trainers = load_json_data("trainers.json")
    print('unimplemented')

_init()
