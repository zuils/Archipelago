import bsdiff4

from worlds.Files import APDeltaPatch


class PokemonFireRedDeltaPatch(APDeltaPatch):
    game = "Pokemon FireRed"
    hash = "51901a6e40661b3914aa333c802e24e8"
    patch_file_ending = ".apfirered"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()
