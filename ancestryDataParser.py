import csv
import json


with open('ancestryData.csv', newline='', encoding='utf-8') as csvfile:
    cbt = csvfile.read().replace("'", "`").replace("\r", "").replace("\t", "")


with open('ancestryclean.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(cbt)


output_set = []
with open('ancestryclean.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        rick = None
        for r in output_set:
            if r["origin"] == row["Origin"]:
                rick = r
                break
        if not rick:
            rick = {"origin": row["Origin"], "size": row["Size"]}
            output_set.append(rick)
        if "traits" not in rick:
            rick["traits"] = []
        rick["traits"].append({
            "name": row["Trait"],
            "desc": row["Desc"].replace("\n", " "),
            "armor": row["Armor Contribution"],
            "HP": row["HP Contribution"],
            "speed": row["Speed "],
        })


with open("ancestrydata.json", "w") as outfile:
    obj = json.dumps(output_set, indent=4)
    outfile.write(obj)


