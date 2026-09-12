from BaseClasses import Item, ItemClassification
from typing import Dict, NamedTuple


OFFSET: int = 20020226000


class PacManWorld2Item(Item):
    game: str = "Pac-Man World 2"


class PacManWorld2ItemData(NamedTuple):
    item_id: int
    category: str
    classification: ItemClassification
    count: int = 1


item_table: Dict[str, PacManWorld2ItemData] = {
    "Progressive Level":    PacManWorld2ItemData(OFFSET, "Levels", ItemClassification.progression, 24),
    "Token":                PacManWorld2ItemData(OFFSET + 1, "Tokens", ItemClassification.progression_deprioritized_skip_balancing, 152),
    "Pac-Dot":              PacManWorld2ItemData(OFFSET + 2, "Filler", ItemClassification.filler)
}