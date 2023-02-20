import csv
import json


with open('supportItemData.csv', newline='', encoding='utf-8') as csvfile:
    cbt = csvfile.read().replace("'", "`").replace("\r", "").replace("\t", "")


with open('ancestryclean.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write(cbt)
