import csv
import json
import re

output_list = []
with open('unitStats.csv', newline='', encoding='utf-8') as csvfile:
    output_dict = {}
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Unit Name"] not in output_dict:
            output_dict[row["Unit Name"]] = {"type": row["Unit Name"], "tiers": []}
        output_dict[row["Unit Name"]]["tiers"].append(
            {
                "tier": row["Tier"],
                "size": row["Size"],
                "armor": row["Armor"],
                "scope": row["Scope"],
                "save": row["Save Target"],
                "init": row["Initiative"],
                "BLK": row["Bulk"],
                "AGI": row["Agility"],
                "MND": row["Mind"],
                "MGK": row["Magic"],
                "HP": row["HP"],
                "dodge": row["Dodge"],
                "speed": row["Speed"],
                "stress": row["Stress Cap"],
                "adef": row["A-Def"], "mana": row["Mana"]
            }
        )

    output_list = list(output_dict.values())

with open("unitStats.json", "w", encoding='utf-8') as outfile:
    obj = json.dumps(output_list , indent=4)
    outfile.write(obj)

