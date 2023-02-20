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
                "type": row["Type"], "action": row["ACTION"], "damage": [], "range": [], "tags": []
            "desc": row["Desc"].replace("\n", "")}

        if "Melee" in temp["profile"] and "Ranged" in temp["profile"]:
            temp["modes"] = {"melee":{}, "ranged": {}}

        dmg_string = row["Combined Damage"].replace("-","").split()


        tags_list = row["Tags"].split(",")
        for taggy in tags_list:
            if taggy == "-" or taggy == "":
                break
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
        temp["effect"] = row["Effect"].replace("\n", " ")
        temp["origin"] = row["Origin"]
        temp["stat_effects"] = {
            "armor": row["Armor Contribution"],
            "speed": row["Speed"],
            "dodge": row["dodge"],
            "save_target": row["Save Target"],
        }
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