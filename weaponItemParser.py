import csv
import json
import re

starting_items = []
unlock_items = []
loot_items = []

with open('weaponItemData.csv', newline='', encoding='utf-8') as csvfile:
    cbt = csvfile.read().replace("'", "`").replace("\r", "").replace("\t", "")

with open('weaponItemDataClean.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(cbt)

with open('weaponItemDataClean.csv', 'r', newline='', encoding='utf-8') as csvfile:
    tags_file = open("tags.json")
    tags_data = json.load(tags_file)
    reader = csv.DictReader(csvfile)

    for row in reader:
        temp = {"name": row["Name"], "profile": row["Melee/Ranged"], "size": row["Size"],
                "type": row["Type"], "action": row["ACTION"], "damage": [], "range": [], "tags": [],
            "desc": row["Desc"].replace("\n", "").replace("\"", "")}

        if "Melee" in temp["profile"] and "Ranged" in temp["profile"]:
            temp["modes"] = {"melee": {}, "ranged": {}}

        dmg_string = row["Combined Damage"].replace("-", "").split()
        if "Melee:" in dmg_string:
            temp["modes"]["melee"]["damage"] = [{'type': dmg_string[2], 'val': dmg_string[1]}]
            temp["modes"]["ranged"]["damage"] = [{'type': dmg_string[5], 'val': dmg_string[4]}]
        else:
            for index, token in enumerate(dmg_string):
                if any(char.isdigit() for char in token):
                    temp["damage"].append({
                        "type": dmg_string[index+1],
                        "val": dmg_string[index]
                    })

        range_string = row["Range/reach"].split()
        if "Melee:" in range_string:
            temp["modes"]["melee"]["range"] = [{'type': range_string[1], 'val': range_string[2]}]
            temp["modes"]["ranged"]["range"] = [{'type': range_string[4], 'val': range_string[5]}]
        elif "or" in range_string:
            try:
                temp["modes"]["melee"]["range"] = [{'type': range_string[0], 'val': range_string[1]}]
                temp["modes"]["ranged"]["range"] = [{'type': range_string[3], 'val': range_string[4]}]
            except Exception as E:
                print(row["Name"])
        else:
            range_string = row["Range/reach"].split(",")
            for element in range_string:
                makeshift = element.split()
                typey = ' '.join(makeshift[:-1])
                val = makeshift[-1]
                temp["range"].append({"type": typey, "val": val})

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
                print (taggy)
                print("L + Ratio")
            temp["tags"].append({
                "id": match_tag,
                "val": val.strip()
            })
        temp["origin"] = row["Origin"]
        match row["Origin"]:
            case "Basic":
                starting_items.append(temp)
            case "Loot":
                loot_items.append(temp)
            case other:
                unlock_items.append(temp)

    tags_file.close()

with open("startingWeaponItems.json", "w") as outfile:
    obj = json.dumps(starting_items, indent=4)
    outfile.write(obj)

with open("unlockWeaponItems.json", "w") as outfile:
    obj = json.dumps(unlock_items, indent=4)
    outfile.write(obj)

with open("lootWeaponItems.json", "w") as outfile:
    obj = json.dumps(loot_items, indent=4)
    outfile.write(obj)