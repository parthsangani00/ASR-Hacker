import csv
import os
import pickle

print("Generating pickle file for databases in Database-CSV directory")
os.chdir("Database-CSV")

dic={}
dic["tableName"] = set()
dic["attributeName"] = set()
dic["attributeValue"] = set()

for file in os.listdir():
    fileName = file.split('.')[0]
    dic["tableName"].add(fileName)

    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        dic["attributeName"].update(fields)
        for row in csvreader:
            dic["attributeValue"].update(row)

os.chdir("../")
file = open('data.pkl', 'wb')
pickle.dump(dic, file)
file.close()


print("Generating pickle file for databases in Database-CSV-Large directory")
os.chdir("Database-CSV-Large")

dic={}
dic["tableName"] = set()
dic["attributeName"] = set()
dic["attributeValue"] = set()

for file in os.listdir():
    fileName = file.split('.')[0]
    dic["tableName"].add(fileName)

    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        dic["attributeName"].update(fields)
        for row in csvreader:
            dic["attributeValue"].update(row)

os.chdir("../")
file = open('data-large.pkl', 'wb')
pickle.dump(dic, file)
file.close()


print("Done")