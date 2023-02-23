import csv
import json

result = []
cbt = ""

with open('classdata.csv', newline='', encoding='utf-8') as csvfile:
    cbt = csvfile.read().replace("'", "`").replace("\r", "").replace("\t", "")

with open('classdataclean.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(cbt)

with open('classdataclean.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        for val in row.values():
            val = val.replace("\"", "").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        if row['Class'] == "--Select Class--" or row['Class'] == "36":
            continue
        new_dict = {}
        new_dict["class"] = row['Class']
        new_dict["role"] = row["Role"]
        new_dict["scope"] = row['Scope']
        new_dict["HP"] = row["HP"]
        new_dict["recoveries"] = row["Recoveries"]
        new_dict["dodge"] = row["Dodge"]
        new_dict["speed"] = row["Speed"]
        new_dict["stress_cap"] = row["Stress Cap"]
        new_dict["memory"] = row["Memory"]
        new_dict["adef"] = row["A-Def"]
        new_dict["mana"] = row["Mana"]
        new_dict["save_target"] = row["Save"]
        new_dict["weapon_slots"] = [
            row["Weapon Slot1"],
            row["Weapon Slot2"],
            row["Weapon Slot3"]
        ]
        new_dict["support_slots"] = [row["Support Slot1"], row["Support Slot2"], row["Support Slot3"], row["Support Slot4"]]
        new_dict["traits"] = [
            {
                "name": row["Trait1"].replace("\n", " "),
                "desc": row["Trait1Desc"].replace("\n", " ")
            }, {"name": row["Trait2"].replace("\n", " "), "desc": row["Trait2Desc"].replace("\n", " ")},
            {"name": row["Trait3"].replace("\n", " "), "desc": row["Trait3Desc"].replace("\n", " ")}
        ]
        if row["TraitReaction"] != "":
            sub_dict = {
                    "name": row["TraitReaction"].replace("\n", " "),
                    "freq": row["TraitReactionFreq"].replace("\n", " "),
                    "trigger": row["TraitReactionTrigger"].replace("\n", " "),
                    "effect": row["TraitReactionEffect"].replace("\n", " ")
                }
            new_dict["traits"].append(sub_dict)
        new_dict["limit_break"] = {
            "name": row["Limit Break"].replace("\n", " "),
            "action": row["Limit Break Action"].replace("\n", " "),
            "desc": row["Limit Break Description"].replace("\n", " ")
        }
        result.append(new_dict)

with open("classdata.json", "w") as outfile:
    obj = json.dumps(result, indent=4)
    outfile.write(obj)

