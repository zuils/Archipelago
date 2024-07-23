from ctypes import *


# Entry in trdata specifies this
class TrainerData:
    type: c_uint8
    trainer_class: c_uint8
    sprite: c_uint8
    party_size: c_uint8
    items: c_uint16
    ai_mask: c_uint32
    battle_type: c_uint32


# Entries in trpoke specify this
class TrainerPokemonData:
    # WHY IS THIS A u16? It's a value from 0-255
    dv: c_uint16
    # WHY IS THIS A u16? 1-100 FITS IN A u8
    level: c_uint16
    # Composite mask of the Pokemon's level (least-significant 10 bits) and form (most-significant 6 bits)
    species: c_uint16
    # Optional
    item: c_uint16
    # Optional
    moves: c_uint16[4]
    seal: c_uint16


# Regular scripts should be PRE-PATCHED as a part of the base patch, this is so we can automate patching.
# There is 2 types of LevelScript. First, IDs 2, 3, and 4 are structured as so:
class LevelScript:
    id: c_uint8
    value: c_int32


# ID 1 type, the type we inject, is structured as so
# Level scripts are padded at the end to fill the word (this is why we need to know the format)
class LevelScriptWithVar:
    id: c_uint8
    # This is ALWAYS 1
    value: c_int32
    padding: c_uint8
    variable_id: c_uint16
    expected_val: c_uint16
    script_id: c_uint32


class LocationEntry:
    tag: str
    connections: list
    access_requirements: list


class ItemEntry:
    tag: str
    long_desc: str
    location: str
    item_flag: int
    vanilla_item: int
    classification: str
    requirements: list[str]


class TriggerEntry:
    tag: str
    location: str
    trigger_flag: int
    trigger_group: str


class TrainerEntry:
    tag: str
    location: str
    flag: int

