import csv
import json
import re

output_list = []

# IN HELL WE LIVE, LAMENT
with open('unitFeaturesData.csv', newline='', encoding='utf-8') as csvfile:
    tags_file = open("tags.json")
    tags_data = json.load(tags_file)
    pattern_action = re.compile(r"\([0-8]\) +[A-Za-z]*", re.M)
    pattern_action_2 = re.compile(r"(Free Action|DEFEND|FULL ATTACK|SKIRMISH|CAST|FIGHT|VOLLEY|BRAWL|REPOSITION|BOLSTER|CHANNEL|Minor|REACTION *(\([A-Za-z0-9/]+\))*)", re.I|re.M)
    pattern_wpn_type = re.compile(r"(Main|Heavy|Light) [A-Za-z]+", re.M)
    pattern_support_type = re.compile(r"(Main|Heavy|Light)", re.M | re.I)
    pattern_x_accuracy = re.compile(r"& \+[0-9] (Accuracy|ACC)", re.M)
    pattern_x_difficulty = re.compile(r"& \+[0-9] (Difficulty|DIF)", re.M)
    pattern_to_hit = re.compile(r"\+[0-9]/\+[0-9]/\+[0-9] +vs +[A-Za-z\-]+", re.M)
    pattern_to_hit_sub_1 = re.compile(r"\+[0-9]")
    pattern_to_hit_sub_2 = re.compile(r"vs [A-Za-z\-]+")
    pattern_scaling_damage = re.compile(r"\[[0-9]+\/[0-9]+\/[0-9]+ [A-Za-z\-]+\]", re.M)
    pattern_scaling_compounddamage = re.compile(r"\[[0-9]+\/[0-9]+\/[0-9]+ [A-Za-z\-]+ \+ [0-9] [A-Za-z\-]+\]", re.M)
    pattern_flat_damage = re.compile(r"\[[0-9|X]+ [A-Za-z]+\]", re.M)
    pattern_recharge = re.compile(r"Recharge [0-9]\+", re.M)
    pattern_ranges = re.compile(r"\[([ A-Za-z]+ [0-9]+|Range = Scope)(,([ A-Za-z]+ [0-9]+)|Range = Scope)*\]", re.M)
    pattern_range_sub = re.compile(r"([ A-Za-z]+ [0-9]+|Range = Scope)", re.M)
    pattern_reliable = re.compile(r"Reliable [0-9]+\/[0-9]+\/[0-9]+", re.M)
    pattern_tags = re.compile(r"[A-Za-z]+ *[0-9|X]* *[(Self)]*", re.M)
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Name"] == "--Select Feature--":
            continue;
        new_feature = {"name": row["Name"].replace("'", "`"), "origin": row["Origin"], "features": {},
                       "effect": row["Effect"].replace("'", "`").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")}
        type_line = re.split(r"[, ]", row["Type"])
        type_line = [element.upper() for element in type_line]
        work_string = row["Top Line"]
        if "TRAIT" in type_line:
            new_feature["type"] = "Trait"
        elif "SKILL" in type_line and "MELEE" in type_line:
            new_feature["type"] = "Melee Skill Attack"
        elif "SKILL" in type_line:
            new_feature["type"] = "Skill"
        elif "SPELL" in type_line and "ATTACK" in type_line:
            new_feature["type"] = "Spell Attack"
        elif "SPELL" in type_line:
            new_feature["type"] = "Spell"
        elif "SUPPORT" in type_line:
            new_feature["type"] = "Support"
            x = re.search(pattern_support_type, work_string)
            if x:
                new_feature["features"]["support_type"] = x.group()
                work_string = re.sub(pattern_support_type, "", work_string)
        elif "WEAPON" in type_line:
            new_feature["type"] = "Ranged Weapon" if "RANGED" in type_line else "Melee Weapon"
            x = re.search(pattern_wpn_type, work_string)
            if x:
                new_feature["features"]["weapon_type"] = x.group()
                work_string = re.sub(pattern_wpn_type, "", work_string)

        x = re.search(pattern_recharge, work_string)
        if x:
            new_feature["features"]["recharge"] = x.group()
            work_string = re.sub(pattern_recharge, "", work_string)
        x = re.search(pattern_action, work_string)
        if x:
            new_feature["features"]["action"] = x.group()
            work_string = re.sub(pattern_action, "", work_string)
        else:
            x = re.search(pattern_action_2, work_string)
            if x:
                new_feature["features"]["action"] = x.group()
                work_string = re.sub(pattern_action_2, "", work_string)
        if "ATTACK" in type_line or "WEAPON" in type_line:
            y = re.search(pattern_x_accuracy, work_string)
            if y:
                new_feature["features"]["to_hit"] = {}
                extract = re.search(pattern_to_hit_sub_1, y.group())
                new_feature["features"]["to_hit"]["accuracy"] = extract.group().strip("+")
                work_string = re.sub(pattern_x_accuracy, "", work_string)

            y = re.search(pattern_x_difficulty, work_string)
            if y:
                new_feature["features"]["to_hit"] = {}
                extract = re.search(pattern_to_hit_sub_1, y.group())
                new_feature["features"]["to_hit"]["difficulty"] = extract.group().strip("+")
                work_string = re.sub(pattern_x_difficulty, "", work_string)

            x = re.search(pattern_to_hit, work_string)
            if x:
                if "to_hit" not in new_feature["features"]:
                    new_feature["features"]["to_hit"] = {}
                to_hits = re.findall(pattern_to_hit_sub_1, x.group())
                versus = re.search(pattern_to_hit_sub_2, x.group()).group().split(" ")[1]
                new_feature["features"]["to_hit"]["defense"] = versus
                for index, value in enumerate(to_hits):
                    new_feature["features"]["to_hit"]["T"+str(index)] = value.strip("+")
                work_string = re.sub(pattern_to_hit, "", work_string)

            x = re.search(pattern_scaling_compounddamage, work_string)
            if x:
                new_feature["features"]["damage"] = {}
                damages = re.findall(r"[0-9]+", x.group())
                typey = re.findall(r"[A-Za-z]+", x.group())
                new_feature["features"]["damage"]["type"] = typey[0]
                new_feature["features"]["damage"]["type_s"] = typey[1]
                for index, dmg in enumerate(damages[:-1]):
                    new_feature["features"]["damage"]["T" + str(index)] = dmg
                new_feature["features"]["damage"]["secondary"] = damages[-1]
                work_string = re.sub(pattern_scaling_compounddamage, "", work_string)

            x = re.search(pattern_scaling_damage, work_string)
            if x:
                new_feature["features"]["damage"] = {}
                damages = re.findall(r"[0-9]+", x.group())
                typey = re.findall(r"[A-Za-z]+", x.group())
                new_feature["features"]["damage"]["type"] = typey
                for index, dmg in enumerate(damages):
                    new_feature["features"]["damage"]["T" + str(index)] = dmg
                work_string = re.sub(pattern_scaling_damage, "", work_string)

                y = re.search(pattern_reliable, work_string)
                if y:
                    damages = re.findall(r"[0-9]+", y.group())
                    new_feature["features"]["tags"] = []
                    new_s = {"id": "tg_reliable"}
                    for index, dmg in enumerate(damages):
                        new_s["T" + str(index)] = dmg
                    new_feature["features"]["tags"].append(new_s)
                    work_string = re.sub(pattern_reliable, "", work_string)
            else:
                x = re.search(pattern_flat_damage, work_string)
                if x:
                    new_feature["features"]["damage"] = {}
                    damages = re.findall(r"[0-9|X]+", x.group())
                    typey = re.findall(r"[A-Za-z]+", x.group())
                    new_feature["features"]["damage"]["type"] = typey
                    new_feature["features"]["damage"]["flat"] = damages[0]
                    work_string = re.sub(pattern_flat_damage, "", work_string)
        ranges = re.search(pattern_ranges, work_string)
        if ranges:
            new_feature["features"]["range"] = []
            sub_ranges = re.findall(re.compile(pattern_range_sub), ranges.group())
            try:
                for rng in sub_ranges:
                    if rng == 'Range = Scope':
                        new_feature["features"]["range"].append(
                            {"type": "Scope",
                                "val": "[SCOPE]"})
                        continue
                    new_feature["features"]["range"].append(
                        {
                            "type": re.search(r"[ A-Za-z]+", rng).group().strip(),
                            "val": re.search(r"[0-9]+", rng).group()
                        }
                    )
                work_string = re.sub(pattern_ranges, "", work_string)
            except Exception as e:
                print(ranges.group())
                raise Exception

        tags_list = re.findall(pattern_tags, work_string)
        if tags_list and "tags" not in new_feature["features"]:
            new_feature["features"]["tags"] = []
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
                #print(new_feature['name'])
                #print(tags_list)
                #print(tag_pair)
                print("L + Ratio")
            new_feature["features"]["tags"].append({"id": match_tag, "val": val.strip()})
        work_string = re.sub(pattern_tags, "", work_string)
        if "type" not in new_feature:
            print(new_feature["name"])
        output_list.append(new_feature)
    tags_file.close()

with open("unitFeatures.json", "w") as outfile:
    obj = json.dumps(output_list, indent=4)
    outfile.write(obj)