import difflib, re
import csv

path = "/Users/fatemenaghshvarian/PycharmProjects/pythonProject2/DCH/KP-internship"
first_file = "/Users/fatemenaghshvarian/PycharmProjects/pythonProject2/DCH/KP-internship/no_date.csv"
second_file = "/Users/fatemenaghshvarian/PycharmProjects/pythonProject2/DCH/KP-internship/date_requiredcsv.csv"

with open(first_file, 'r') as t1, open(second_file, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

with open('update.csv', 'w') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)