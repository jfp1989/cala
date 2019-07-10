#!/usr/bin/python

import csv, json

csvFilePath = "people.csv"
jsonFilePath = "peopleJson.json"

#Read the file .csv and add the data to a dictionary
data = {}
with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for csvRow in csvReader:
        id = csvRow['id']
        data[id] = csvRow

#write data to a json file
with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))