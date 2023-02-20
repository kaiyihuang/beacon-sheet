import csv
import json
import re

starting_items = []
unlock_items = []
loot_items = []

with open('techniquesData.csv', newline='', encoding='utf-8') as csvfile:
    cbt = csvfile.read().replace("'", "`").replace("\r", "").replace("\t", "")

with open('techniquesDataClean.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(cbt)

with open('techniquesDataClean.csv', 'r', newline='', encoding='utf-8') as csvfile:
    tags_file = open("tags.json")
    tags_data = json.load(tags_file)
    reader = csv.DictReader(csvfile)

    for row in reader:
        temp = {"name": row["Name"], "profile": row["Melee/Ranged"], "memory_cost": row["MEM"],
                "type": row["Type"], "action": row["Action"], "damage": [], "range": [], "tags": [],
                "effects": row["Effects"].replace("\n", "").replace("\"", ""),
                "origin": row["Source"],
                "stat_effects": {"armor": row["Armor Contribution"], "hp": row["HP Contribution"],
                                 "mana": row["mana contribution"], "speed": row["speed"],
                                 "dodge": row["dodge"]}}

        range_string = row["range"].replace("[", "").replace("]", "").split(",")
        for element in range_string:
            if len(range_string) < 2:
                break
            makeshift = element.split()
            typey = ' '.join(makeshift[:-1])
            val = makeshift[-1]
            if typey == "Scope =":
                temp["range"].append({"type": "Scope", "val": "[SCOPE]"})
            else:
                temp["range"].append({"type": typey, "val": val})

        dmg_string = row["Damage"].replace("-", "").split()
        for index, token in enumerate(dmg_string):
            if len(dmg_string) < 2:
                break
            if any(char.isdigit() for char in token):
                temp["damage"].append({"type": dmg_string[index + 1], "val": dmg_string[index]})

        match row["Source"]:
            case "Basic":
                starting_items.append(temp)
            case "Loot":
                loot_items.append(temp)
            case other:
                unlock_items.append(temp)

with open("startingTechniques.json", "w") as outfile:
    obj = json.dumps(starting_items, indent=4)
    outfile.write(obj)

with open("unlockTechniques.json", "w") as outfile:
    obj = json.dumps(unlock_items, indent=4)
    outfile.write(obj)

with open("lootTechniques.json", "w") as outfile:
    obj = json.dumps(loot_items, indent=4)
    outfile.write(obj)