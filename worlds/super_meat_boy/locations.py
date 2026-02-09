from typing import List, Dict, NamedTuple
from BaseClasses import Location
from .utils import load_json_data

OFFSET: int = 30112010000


class SMBLocation(Location):
    game: str = "Super Meat Boy"


class SMBLocationData(NamedTuple):
    location_id: int
    category: List[str]
    region: str
    requirement: str


location_json = load_json_data("locations.json")
location_id: int = 1
location_table: Dict[str, SMBLocationData] = {}

for l in location_json:
    location_table[l["name"]] = SMBLocationData(location_id + OFFSET, l.get("category", []), l.get("region", "Initial"), l.get("requires", ""))
    location_id += 1
