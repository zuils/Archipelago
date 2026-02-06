from typing import List, Dict, NamedTuple, TYPE_CHECKING
from BaseClasses import Item, ItemClassification
from .utils import load_json_data

if TYPE_CHECKING:
    from . import SMBWorld

OFFSET: int = 20101130000


class SMBItem(Item):
    game: str = "Super Meat Boy"


class SMBItemData(NamedTuple):
    item_id: int
    category: List[str]
    classification: ItemClassification
    count: int


items_json = load_json_data("items.json")
item_id: int = 1
item_table: Dict[str, SMBItemData] = {}
item_name_groups: Dict[str, list[str]] = {}

def parse_classification(val: str) -> ItemClassification:
    if val == "progression_deprioritized_skip_balancing":
        return ItemClassification.progression_deprioritized_skip_balancing
    elif val == "progression":
        return ItemClassification.progression
    elif val == "useful":
        return ItemClassification.useful
    elif val == "filler":
        return ItemClassification.filler
    else:
        raise ValueError(f"Invalid ItemClassification: {val}")


for i in items_json:
    item_table[i["name"]] = SMBItemData(item_id + OFFSET, i["category"], parse_classification(i["classification"]), i["count"])
    item_id += 1
    
    for cat in i["category"]:
        item_name_groups[cat] = item_name_groups.get(cat, []) + [i["name"]]