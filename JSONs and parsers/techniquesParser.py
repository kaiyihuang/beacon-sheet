import csv
import json
import re

starting_items = []
unlock_items = []
loot_items = []

with open('techniquesData.csv', newline='', encoding='utf-8') as csvfile:
    cbt = csvfile.read().replace("'", "`")

with open('techniquesDataClean.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(cbt)

with open('techniquesDataClean.csv', 'r', newline='', encoding='utf-8') as csvfile:
    tags_file = open("tags.json")
    tags_data = json.load(tags_file)
    reader = csv.DictReader(csvfile)

    for row in reader:
        temp = {"name": row["Name"], "profile": row["Melee/Ranged"], "memory_cost": row["MEM"],
                "type": row["Type"], "action": row["Action"], "damage": [], "range": [], "tags": [],
                "effects": row["Effects"].replace("\"", "").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t"),
                "origin": row["Source"],
                "stat_effects": {"armor": row["Armor Contribution"], "hp": row["HP Contribution"],
                                 "mana": row["mana contribution"], "speed": row["speed"],
                                 "dodge": row["dodge"]}}

        range_string = row["range"].replace("[", "").replace("]", "").split(",")
        if "Hinder" in row["Name"]:
            print(range_string)
        for element in range_string:

            makeshift = element.split()
            if len(makeshift) < 2:
                break
            typey = ' '.join(makeshift[:-1])
            val = makeshift[-1]

            if typey == "Scope =":
                temp["range"].append({"type": "Scope", "val": "[SCOPE]"})
            else:
                temp["range"].append({"type": typey, "val": val})

        dmg_string = row["Damage"].replace("-", "").split()
        for index, token in enumerate(dmg_string):
            if not dmg_string:
                break
            if any(char.isdigit() for char in token):
                temp["damage"].append({"type": dmg_string[index + 1], "val": dmg_string[index]})

        tags_list = row["Tags"].split(",")
        for taggy in tags_list:
            if taggy == "-" or taggy == "":
                break
            if taggy == 'AP':
                taggy = "PIERCING"
            tag_pair = taggy.strip().split(" ")
            name = tag_pair[0]
            val = tag_pair[1] if len(tag_pair) > 1 else ""
            name_regex = taggy.strip().upper().replace("(", "(").replace(")", ")")
            name_regex = re.sub("[0-9|X]", "{VAL}", name_regex)
            try:
                match_tag = next(x["id"] for x in tags_data if x["name"] == name_regex)
            except Exception as e:
                print(taggy)
                print("L + Ratio")
            temp["tags"].append({"id": match_tag, "val": val.strip()})

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