import json

textP1 = [
    {
        "count": "20",
        "name": "Chapter 1 LW Level Completion",
        "category": ["LW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 1 DW Level Completion",
        "category": ["DW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 2 LW Level Completion",
        "category": ["LW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 2 DW Level Completion",
        "category": ["DW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 3 LW Level Completion",
        "category": ["LW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 3 DW Level Completion",
        "category": ["DW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 4 LW Level Completion",
        "category": ["LW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 4 DW Level Completion",
        "category": ["DW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 5 LW Level Completion",
        "category": ["LW Levels"],
        "progression": "true"
    },
    {
        "count": "20",
        "name": "Chapter 5 DW Level Completion",
        "category": ["DW Levels"],
        "progression": "true"
    },
    {
        "count": "5",
        "name": "Chapter 6 LW Level Completion",
        "category": ["LW Levels"],
        "progression": "true"
    },
    {
        "count": "5",
        "name": "Chapter 6 DW Level Completion",
        "category": ["DW Levels"],
        "progression": "true"
    },
    {
        "count": "1",
        "name": "Chapter 1 Boss Completion",
        "category": ["Boss"],
        "progression": "true"
    },
    {
        "count": "1",
        "name": "Chapter 2 Boss Completion",
        "category": ["Boss"],
        "progression": "true"
    },
    {
        "count": "1",
        "name": "Chapter 3 Boss Completion",
        "category": ["Boss"],
        "progression": "true"
    },
    {
        "count": "1",
        "name": "Chapter 4 Boss Completion",
        "category": ["Boss"],
        "progression": "true"
    },
    {
        "count": "1",
        "name": "Chapter 5 Boss Completion",
        "category": ["Boss"],
        "progression": "true"
    },
    {
        "count": "1",
        "name": "Chapter 6 LW Boss Completion",
        "category": ["Boss"],
        "progression": "true"
    }
]

textP3 = [
    {
        "count": "1",
        "name": "8-Bit Meat Boy",
        "category": ["Character"],
        "filler": "true"
    },
    {
        "count": "1",
        "name": "4-Bit Meat Boy",
        "category": ["Character"],
        "filler": "true"
    },
    {
        "count": "1",
        "name": "4-Color Meat Boy",
        "category": ["Character"],
        "filler": "true"
    },
    {
        "count": "1",
        "name": "Meat Ninja",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Commander Video",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Jill",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Ogmo",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Flywrench",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "The Kid",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Tim",
        "category": ["Character"],
        "filler": "true"
    },
    {
        "count": "1",
        "name": "Headcrab",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Josef",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Naija",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "RunMan",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Captain Viridian",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Steve",
        "category": ["Character"],
        "useful": "true"
    },
    {
        "count": "1",
        "name": "Tofu Boy",
        "category": ["Character"],
        "filler": "true"
    },
    {
        "count": "1",
        "name": "Goo Ball",
        "category": ["Character"],
        "filler": "true"
    }
]

textP2 = []

for i in range(1, 6):
    for j in range(1, 21):
        textP2.append({
            "count": "1",
            "name": f"{i}-{j} A+ Rank",
            "category": [f"Chapter {i} A+ Rank"],
            "progression": "true"
        })

for i in range(1, 6):
    textP2.append({
        "count": "1",
        "name": f"6-{i} A+ Rank",
        "category": ["Chapter 6 A+ Rank"],
        "progression": "true"
    })

textP1.extend(textP2)
textP1.extend(textP3)

with open("./data/items.json", 'w') as f:
    f.write(json.dumps(textP1, indent=4))
