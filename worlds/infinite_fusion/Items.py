from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class IFItem(Item):
    game: str = "Pokemon Infinite Fusion"


class IFItemData(NamedTuple):
    category: str
    item_id: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1


def get_items_by_category(category: str) -> Dict[str, IFItemData]:
    item_dict: Dict[str, IFItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict


item_table: Dict[str, IFItemData] = {
    # Key Items
    "Town Map": IFItemData("Key Item", 766784_000, ItemClassification.progression_skip_balancing),
    "Bicycle": IFItemData("Key Item", 766784_001, ItemClassification.progression),
    "Pokedex": IFItemData("Key Item", 766784_002, ItemClassification.progression),
    "Card Key": IFItemData("Key Item", 766784_003, ItemClassification.progression),
    "S.S. Ticket": IFItemData("Key Item", 766784_004, ItemClassification.progression),
    "Gold Teeth": IFItemData("Key Item", 766784_005, ItemClassification.progression),
    "Oak's Parcel": IFItemData("Key Item", 766784_006, ItemClassification.progression),
    "Item Finder": IFItemData("Key Item", 766784_007, ItemClassification.progression),
    "Silph Scope": IFItemData("Key Item", 766784_008, ItemClassification.progression),
    "Poke Flute": IFItemData("Key Item", 766783_009, ItemClassification.progression),
    "Lift Key": IFItemData("Key Item", 766784_010, ItemClassification.progression),
    "Exp. All": IFItemData("Key Item", 766784_011, ItemClassification.progression_skip_balancing),
    "Old Rod": IFItemData("Key Item", 766784_012, ItemClassification.useful),

    # Badges
    "Boulder Badge": IFItemData("Badge", 766784_003, ItemClassification.progression),
    "Cascade Badge": IFItemData("Badge", 766784_004, ItemClassification.progression),
    "Thunder Badge": IFItemData("Badge", 766784_005, ItemClassification.progression),
    "Rainbow Badge": IFItemData("Badge",),

    # Misc
    "Master Ball": IFItemData("Poke Ball", 766784_000, ItemClassification.useful),
    "Ultra Ball": IFItemData("Poke Ball", 766784_001),
    "Great Ball": IFItemData("Poke Ball", 766784_002),
    "Poke Ball": IFItemData("Poke Ball", 766784_003),
    "Moon Stone": IFItemData("Evolution Stone", 766784_007, ItemClassification.useful),
    "Antidote": IFItemData("Consumable", 766784_008),
    "Burn Heal": IFItemData("Consumable", 766784_009),
    "Ice Heal": IFItemData("Consumable", 766784_010),
    "Awakening": IFItemData("Consumable", 766784_011),
    "Paralyze Heal": IFItemData("Consumable", 766784_012),
    "Full Restore": IFItemData("Consumable", 766784_013),
    "Max Potion": IFItemData("Consumable", 766784_014),
    "Hyper Potion": IFItemData("Consumable", 766784_015),
    "Super Potion": IFItemData("Consumable", 766784_016),
    "Potion": IFItemData("Consumable", 766784_017)
}
