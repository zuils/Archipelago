import json

locations = [
    {
        "name": "1-1 Hello World",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-2 Upward",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-3 The Gap",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-4 Nutshell",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-5 Holy Mountain",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-WZ Sky Pup",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-6 Bladecatcher",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-7 Diverge",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-8 The Bit",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-9 Safety Third",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-10 The Leevee",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-11 Fired",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-12 Revolve",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-WZ The Commander!",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-13 Tommy's Cabin",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-14 Blood Mountain",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-15 Cactus Jumper",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-16 Sidewinder",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-17 Morningstar",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-18 Altamont",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-19 Intermission",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-WZ Hand Held Hack",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-20 The Test",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": []
    },
    {
        "name": "1-Boss Lil' Slugger",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": "|Chapter 1 Level Completion:17|"
    },
    {
        "name": "-1 |> ._. |>",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Light World"],
                "requires": "|Chapter 1 Boss Completion|"
    },
    {
        "name": "1-1X Oh, Hello",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-1 A+ Rank|"
    },
    {
        "name": "1-2X Onward",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-2 A+ Rank|"
    },
    {
        "name": "1-3X Bzzzzz",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-3 A+ Rank|"
    },
    {
        "name": "1-4X Plum Rain",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-4 A+ Rank|"
    },
    {
        "name": "1-5X Creamsoda",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-5 A+ Rank|"
    },
    {
        "name": "1-6X I Am The Night",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-6 A+ Rank|"
    },
    {
        "name": "1-7X Two Roads",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-7 A+ Rank|"
    },
    {
        "name": "1-8X Big Red",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-8 A+ Rank|"
    },
    {
        "name": "1-9X So Close",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-9 A+ Rank|"
    },
    {
        "name": "1-10X Walls",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-10 A+ Rank|"
    },
    {
        "name": "1-11X Doused",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-11 A+ Rank|"
    },
    {
        "name": "1-12X Fireal",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-12 A+ Rank|"
    },
    {
        "name": "1-13X Tommy's Condo",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-13 A+ Rank|"
    },
    {
        "name": "1-WZ Space Boy",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-13 A+ Rank|"
    },
    {
        "name": "1-14X Mystery Spot",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-14 A+ Rank|"
    },
    {
        "name": "1-15X Kick Machine",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-15 A+ Rank|"
    },
    {
        "name": "1-16X Night Game",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-16 A+ Rank|"
    },
    {
        "name": "1-17X The Clock",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-17 A+ Rank|"
    },
    {
        "name": "1-18X Whitewash",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-18 A+ Rank|"
    },
    {
        "name": "1-19X The Queener",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-19 A+ Rank|"
    },
    {
        "name": "1-20X A Perfect End",
        "region": "Chapter 1: The Forest",
                "category": ["Chapter 1 Dark World"],
                "requires": "|1-20 A+ Rank|"
    },
    {
        "name": "2-1 Biohazard",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-2 One Down",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-3 Memories",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-4 Blow",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-5 Big Empty",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-6 The Grain",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-7 Hush",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-8 The Sabbath",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-WZ The Bootlicker!",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-9 Blood Swamp",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-10 Johnny's Cage",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-11 Ghost Key",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-12 Above",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-WZ Castle Crushers",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-13 Ulcer Pop",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-14 Aunt Flo",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-15 Gallbladder",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-WZ The Blood Shed",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-16 Synj",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-17 Worm Food",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-18 Destructoid",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-19 Six Feet",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-20 Day Breaker",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": []
    },
    {
        "name": "2-Boss C.H.A.D.",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Light World"],
                "requires": "|Chapter 2 Level Completion:17|"
    },
    {
        "name": "-2 |> ._. |>",
        "category": ["Chapter 2 Light World"],
                "requires": "|Chapter 2 Boss Completion|",
                "region": "Chapter 2: The Hospital"
    },
    {
        "name": "2-1X Back Track",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-1 A+ Rank|"
    },
    {
        "name": "2-2X Pinkeye Falls",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-2 A+ Rank|"
    },
    {
        "name": "2-3X Buzzzzcut",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-3 A+ Rank|"
    },
    {
        "name": "2-4X Blown",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-4 A+ Rank|"
    },
    {
        "name": "2-5X Agent Orange",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-5 A+ Rank|"
    },
    {
        "name": "2-WZ 1977",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-5 A+ Rank|"
    },
    {
        "name": "2-6X Cher Noble",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-6 A+ Rank|"
    },
    {
        "name": "2-7X The Moon",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-7 A+ Rank|"
    },
    {
        "name": "2-8X Grape Soda",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-8 A+ Rank|"
    },
    {
        "name": "2-9X Centipede",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-9 A+ Rank|"
    },
    {
        "name": "2-10X The Kracken",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-10 A+ Rank|"
    },
    {
        "name": "2-11X Spineless",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-11 A+ Rank|"
    },
    {
        "name": "2-12X Grey Matter",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-12 A+ Rank|"
    },
    {
        "name": "2-13X Dust Bunnies",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-13 A+ Rank|"
    },
    {
        "name": "2-14X Crawl Space",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-14 A+ Rank|"
    },
    {
        "name": "2-15X Insurance?",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-15 A+ Rank|"
    },
    {
        "name": "2-16X P.S.Y.",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-16 A+ Rank|"
    },
    {
        "name": "2-17X Nels Box",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-17 A+ Rank|"
    },
    {
        "name": "2-18X Electrolysis",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-18 A+ Rank|"
    },
    {
        "name": "2-19X Tenebrae",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-19 A+ Rank|"
    },
    {
        "name": "2-20X Solemnity",
        "region": "Chapter 2: The Hospital",
                "category": ["Chapter 2 Dark World"],
                "requires": "|2-20 A+ Rank|"
    },
    {
        "name": "3-1 Pit Stop",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-2 The Salt Lick",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-3 Push",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-4 Transmissions",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-5 Uptown",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-WZ Cartridge Dump",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-6 The Shaft",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-7 Mind the Gap",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-WZ Tunnel Vision",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-8 Boomtown",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-9 Shotzie!",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-10 Breakdown",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-11 Box Tripper",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-12 The Dumper",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-13 The Bend",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-14 Gurdy",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-15 Vertigo",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-16 Mono",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-WZ The Jump Man!",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-17 Rustic",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-18 The Grundle",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-19 Dig",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-20 White Noise",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": []
    },
    {
        "name": "3-Boss Brownie",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": "|Chapter 3 Level Completion:17|"
    },
    {
        "name": "-3 |> ._. |>",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Light World"],
                "requires": "|Chapter 3 Boss Completion|"
    },
    {
        "name": "3-1X Step One",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-1 A+ Rank|"
    },
    {
        "name": "3-2X Salt + Wound",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-2 A+ Rank|"
    },
    {
        "name": "3-3X The Red Room",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-3 A+ Rank|"
    },
    {
        "name": "3-4X Assemble",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-4 A+ Rank|"
    },
    {
        "name": "3-5X Wasp",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-5 A+ Rank|"
    },
    {
        "name": "3-6X Not You Again",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-6 A+ Rank|"
    },
    {
        "name": "3-7X Pluck",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-7 A+ Rank|"
    },
    {
        "name": "3-8X Salt Crown",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-8 A+ Rank|"
    },
    {
        "name": "3-WZ Kontra",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-8 A+ Rank|"
    },
    {
        "name": "3-9X Goliath",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-9 A+ Rank|"
    },
    {
        "name": "3-10X Exploder",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-10 A+ Rank|"
    },
    {
        "name": "3-11X The Salt Man",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-11 A+ Rank|"
    },
    {
        "name": "3-12X Hellevator",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-12 A+ Rank|"
    },
    {
        "name": "3-13X Black Circle",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-13 A+ Rank|"
    },
    {
        "name": "3-14X Salmon",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-14 A+ Rank|"
    },
    {
        "name": "3-15X Vertebreaker",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-15 A+ Rank|"
    },
    {
        "name": "3-16X The Chaser",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-16 A+ Rank|"
    },
    {
        "name": "3-17X Ashes",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-17 A+ Rank|"
    },
    {
        "name": "3-18X Bile Duct",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-18 A+ Rank|"
    },
    {
        "name": "3-19X El Topo",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-19 A+ Rank|"
    },
    {
        "name": "3-20X Sweet Pea",
        "region": "Chapter 3: The Salt Factory",
                "category": ["Chapter 3 Dark World"],
                "requires": "|3-20 A+ Rank|"
    },
    {
        "name": "4-1 Boilermaker",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-2 Brindle",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-3 Heck Hole",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-4 Hex",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-5 Pyro",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-6 Leviathan",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-7 Rickets",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-8 Weibe",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-WZ Brimstone",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-9 Deceiver",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-10 Ball N Chain",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-11 Oracle",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-12 Big Brother",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-13 Lazy",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-14 Adversary",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-WZ The Key Master",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-15 Abaddon",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-16 Bow",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-17 Lost Highway",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-18 Boris",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-WZ The Fly Guy!",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-19 The Hive",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-20 Babylon",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": []
    },
    {
        "name": "4-Boss Little Horn",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": "|Chapter 4 Level Completion:17|"
    },
    {
        "name": "-4 |> ._. |>",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Light World"],
                "requires": "|Chapter 4 Boss Completion|"
    },
    {
        "name": "4-1X Gretel",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-1 A+ Rank|"
    },
    {
        "name": "4-2X Golgotha",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-2 A+ Rank|"
    },
    {
        "name": "4-3X Char",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-3 A+ Rank|"
    },
    {
        "name": "4-4X Altered",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-4 A+ Rank|"
    },
    {
        "name": "4-5X Wicked One",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-5 A+ Rank|"
    },
    {
        "name": "4-6X The Gnashing",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-6 A+ Rank|"
    },
    {
        "name": "4-7X Thistle",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-7 A+ Rank|"
    },
    {
        "name": "4-WZ MMMMMM",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-7 A+ Rank|"
    },
    {
        "name": "4-8X Billy Boy",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-8 A+ Rank|"
    },
    {
        "name": "4-9X Glut",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-9 A+ Rank|"
    },
    {
        "name": "4-10X Gallow",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-10 A+ Rank|"
    },
    {
        "name": "4-11X Surrender",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-11 A+ Rank|"
    },
    {
        "name": "4-12X Surrender",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-12 A+ Rank|"
    },
    {
        "name": "4-13X Oblivion",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-13 A+ Rank|"
    },
    {
        "name": "4-14X Old Scratch",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-14 A+ Rank|"
    },
    {
        "name": "4-15X Bone Yard",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-15 A+ Rank|"
    },
    {
        "name": "4-16X Starless",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-16 A+ Rank|"
    },
    {
        "name": "4-17X Invocation",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-17 A+ Rank|"
    },
    {
        "name": "4-18X Sag Chamber",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-18 A+ Rank|"
    },
    {
        "name": "4-19X Long Goodbye",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-19 A+ Rank|"
    },
    {
        "name": "4-20X Imperial",
        "region": "Chapter 4: Hell",
                "category": ["Chapter 4 Dark World"],
                "requires": "|4-20 A+ Rank|"
    },
    {
        "name": "5-1 The Witness",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-WZ Skyscraper",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-2 Evangel",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-3 Ripe Decay",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-4 Rise",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-5 Panic Switch",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-6 Left Behind",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-7 The Fallen",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-WZ The Guy!",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-8 Descent",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-9 Abomination",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-10 Grinding Mill",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-11 Heretic",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-12 10 Horns",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-WZ Sunshine Island",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-13 The Lamb",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-14 King Carrion",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-15 The Flood",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-16 Rotgut",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-17 The Kingdom",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-18 Gate of Ludd",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-19 Wrath",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-20 Judgement",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": []
    },
    {
        "name": "5-Boss Larries Lament",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": "|Chapter 5 Level Completion:17|"
    },
    {
        "name": "-5 |> ._. |>",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Light World"],
                "requires": "|Chapter 5 Boss Completion|"
    },
    {
        "name": "5-1X The Clot",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-1 A+ Rank|"
    },
    {
        "name": "5-2X Loomer",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-2 A+ Rank|"
    },
    {
        "name": "5-3X Spank",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-3 A+ Rank|"
    },
    {
        "name": "5-4X Alabaster",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-4 A+ Rank|"
    },
    {
        "name": "5-5X Nix",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-5 A+ Rank|"
    },
    {
        "name": "5-6X Ripcord",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-6 A+ Rank|"
    },
    {
        "name": "5-7X Downpour",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-7 A+ Rank|"
    },
    {
        "name": "5-8X Downer",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-8 A+ Rank|"
    },
    {
        "name": "5-9X Swine",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-9 A+ Rank|"
    },
    {
        "name": "5-10X Pulp Factory",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-10 A+ Rank|"
    },
    {
        "name": "5-11X Blight",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-11 A+ Rank|"
    },
    {
        "name": "5-12X Canker",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-12 A+ Rank|"
    },
    {
        "name": "5-13X Halo of Flies",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-13 A+ Rank|"
    },
    {
        "name": "5-14X Necrosis",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-14 A+ Rank|"
    },
    {
        "name": "5-15X Choke",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-15 A+ Rank|"
    },
    {
        "name": "5-16X Coil",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-16 A+ Rank|"
    },
    {
        "name": "5-17X Millenium",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-17 A+ Rank|"
    },
    {
        "name": "5-18X Stain",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-18 A+ Rank|"
    },
    {
        "name": "5-19X Magog",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-19 A+ Rank|"
    },
    {
        "name": "5-20X Quietus",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-20 A+ Rank|"
    },
    {
        "name": "5-WZ Meat is Death",
        "region": "Chapter 5: The Rapture",
                "category": ["Chapter 5 Dark World"],
                "requires": "|5-20 A+ Rank|"
    },
    {
        "name": "6-1 The Pit",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Light World"],
                "requires": []
    },
    {
        "name": "6-2 Schism",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Light World"],
                "requires": []
    },
    {
        "name": "6-3 Echoes",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Light World"],
                "requires": []
    },
    {
        "name": "6-4 Gently",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Light World"],
                "requires": []
    },
    {
        "name": "6-5 Omega",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Light World"],
                "requires": []
    },
    {
        "name": "6-Boss Dr. Fetus",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Light World"],
                "requires": "|Chapter 1 Boss Completion| AND |Chapter 2 Boss Completion| AND |Chapter 3 Boss Completion| AND |Chapter 4 Boss Completion| AND |Chapter 5 Boss Completion| AND |Chapter 6 Level Completion:5|"
    },
    {
        "name": "-6 |> ._. |>",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Light World"],
                "requires": "|Chapter 6 LW Boss Completion|"
    },
    {
        "name": "6-1X Detox",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Dark World"],
                "requires": "|6-1 A+ Rank|"
    },
    {
        "name": "6-2X Ghost Tomb",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Dark World"],
                "requires": "|6-2 A+ Rank|"
    },
    {
        "name": "6-3X From Beyond",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Dark World"],
                "requires": "|6-3 A+ Rank|"
    },
    {
        "name": "6-4X Maze of Ith",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Dark World"],
                "requires": "|6-4 A+ Rank|"
    },
    {
        "name": "6-5X No Quarter",
        "region": "Chapter 6: The End",
                "category": ["Chapter 6 Dark World"],
                "requires": "|6-5 A+ Rank|"
    },
    {
        "name": "6-BossX Dr. Fetus",
        "region": "Chapter 6: The End",
                "victory": "true",
                "category": ["Chapter 6 Dark World"],
                "requires": "|@DW Levels:85|"
    }
]

modified_locations = []

for location in locations:
    name = location["name"].split(" ")[0].split("-")
    if name[0].isdigit() and name[1].isdigit():
        # print(location["name"])
        modified_location = location.copy()
        modified_location["name"] += " (A+ Rank)"
        modified_locations.extend([location, modified_location])
    else:
        modified_locations.append(location)

with open('./data/locations.json', 'w') as f:
    f.write(json.dumps(modified_locations, indent=4))
