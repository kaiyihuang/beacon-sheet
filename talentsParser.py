import csv
import json
import re

with open('talentsData.csv', newline='', encoding='utf-8') as csvfile:
    cbt = csvfile.read().replace("'", "`").replace("\r", " ").replace("\t", " ")


with open('talentsClean.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(cbt)

output = []
with open('talentsClean.csv', 'r', newline='', encoding='utf-8') as csvfile:
    tags_file = open("tags.json")
    tags_data = json.load(tags_file)
    reader = csv.DictReader(csvfile)
    for row in reader:
        output.append(
            {
                "id": row["uniqueID"],
                "talent": row["Talent"],
                "name": row["Name"],
                "effect": row["Effect"].replace("\n", "\u0085"),
                "rank": row["Rank "],
            }
        )
with open("talents.json", "w", encoding='utf-8') as outfile:
    obj = json.dumps(output, indent=4)
    outfile.write(obj)