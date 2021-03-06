import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import re
import numpy as np
from json import dumps


from pandas import DataFrame
import sys
import openpyxl



endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?item ?itemLabel 
WHERE {
  ?item wdt:P5935 ?id;
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
}
LIMIT 1000"""





def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()





results = get_results(endpoint_url, query)  # all the productions save in json format.





def get_production_label_without_date(result):
    season_regex = re.compile(r'\(\d{4}-\d{4}\)')
    season = season_regex.findall(result["itemLabel"]["value"]).pop()
    begin_year = int(season.split("-")[0][1:])
    end_year = int(season.split("-")[-1][:-1])
    production = re.sub(r'\([^)]*\)', '', result["itemLabel"]["value"])
    production = production.strip() if production.strip() != "" else None
    return (production, begin_year, end_year)




productions_seasons = [get_production_label_without_date(result) for result in results["results"]["bindings"]]




labels_without_dates = set([ps[0] for ps in productions_seasons])  # this is the full set of productions that you get




print(len(labels_without_dates))




production_groups = {label: {"entities": [], "years": []} for label in
                     labels_without_dates}  # this will become the dictionary in which you store the groups of productions, c.q. reruns; the key will be the label_without_date, the value will be an array of productions; I used dict comprehension here, see https://docs.python.org/3/tutorial/datastructures.html#dictionaries




production_groups = {label: {"entities": [], "years": []} for label in labels_without_dates}




print(len(production_groups))




for label in labels_without_dates:
    for result in results["results"]["bindings"]:
        production_label_without_date, begin_year, end_year = get_production_label_without_date(
            result)  # this is some function that gets the label of a production without season info, should be the same code that is used to make labels_without_dates
        if label == production_label_without_date:
            production_groups[label]["entities"].append((result["item"]["value"], result["itemLabel"]["value"]))
            production_groups[label]["years"].append(begin_year)
            production_groups[label]["years"].append(end_year)



print(len(production_groups))




# arr=[]
data = []

for production_group in production_groups:
    production = production_groups[production_group]
    arr = []
    if len(production["years"]) > 2:
        arr.append(production["entities"])
        arr.append(production["years"])
        # print(production["years"])
        # print(type())
        # arr.append(max(production["years"])
        # new=arr[1].sort()
        # print(new)
    data.append(arr)

    arr = []

print(data)
df = pd.DataFrame(data)

# dict(sorted(production_groups.items(), key=lambda item: item['years']))





newdf = df.dropna()



newdf.to_csv('export_dataframe.csv', index=False, header=True)





# newdf.loc[url]




def get_names(newdf):
    i = 0
    names = []
    pris = []
    for url in newdf[0]:
        line = url[0][0]
        name1 = url[0][1]
        name2 = url[1][1]
        x = name1.split("(")
        lenx = len(x) - 1
        sname1 = name1.split("(")[lenx].split(")")[0].split("-")[0]
        sname2 = name2.split("(")[lenx].split(")")[0].split("-")[0]
        intsname1 = float(sname1)
        intsname2 = float(sname2)
        if (intsname1 < intsname2):
            line2 = url[0][0]
        else:
            line2 = url[1][0]
        words = line2.split("/")
        name = words[4]
        names.append(name)

    return names


######for each name append 2 for End and start file:
def get_names_start_end(newdf):
    i = 0
    names = []
    pris = []
    for url in newdf[0]:
        line = url[0][0]
        name1 = url[0][1]
        name2 = url[1][1]
        x = name1.split("(")
        lenx = len(x) - 1
        sname1 = name1.split("(")[lenx].split(")")[0].split("-")[0]
        sname2 = name2.split("(")[lenx].split(")")[0].split("-")[0]
        intsname1 = float(sname1)
        intsname2 = float(sname2)
        if (intsname1 < intsname2):
            line2 = url[0][0]
        else:
            line2 = url[1][0]
        words = line2.split("/")
        name = words[4]
        names.append(name)
        names.append(name)

    return names





descriptions = []
for x in newdf[1]:
    fromT = min(x)
    ToT = max(x)
    des = "from " + str(fromT) + " until " + str(ToT)
    descriptions.append(des)
print(type(descriptions))
print(get_names(newdf))




d = {"name": get_names(newdf), "descriptions": descriptions}




Descriptioin_export = pd.DataFrame(d)




Descriptioin_export.to_excel("Descriptioin_export.xlsx")




# start_time ----- EndTime
print(get_names_start_end(newdf))




dates = []
for x in newdf[1]:
    fromT = min(x)
    ToT = max(x)
    dates.append(fromT)
    dates.append(ToT)
print(dates)
Test = []
n = 0
x1 = 'P580'
x2 = 'P582'
for n in range(int(len(newdf[1]))):
    Test.append(x1)
    Test.append(x2)
print(Test)




dd = {"name": get_names_start_end(newdf), "x": Test, "year": dates}




End_Start_export = pd.DataFrame(dd)




End_Start_export.to_excel("End_Start_export.xlsx")



# lable without dates:


i = 0
labels = []
for url in newdf[0]:
    # print(url[0][0])
    line = url[1][1]
    words = line.split("(")
    print(words[0])
    label = words[0]
    labels.append(label)

print(labels)
LDUs = []
for n in range(int(len(newdf[1]))):
    LDUs.append('ldu')




ddd = {"name": get_names(newdf), "LDUs": LDUs, "labels": labels}

lable_without_dates = pd.DataFrame(ddd)
lable_without_dates.to_excel("lable_without_dates.xlsx")










# merg:

def get_merge(newdf):
    i = 0
    source = []
    destination = []
    for url in newdf[0]:
        line = url[0][0]
        name1 = url[0][1]
        name2 = url[1][1]
        x = name1.split("(")
        lenx = len(x) - 1
        sname1 = name1.split("(")[lenx].split(")")[0].split("-")[0]
        sname2 = name2.split("(")[lenx].split(")")[0].split("-")[0]
        intsname1 = float(sname1)
        intsname2 = float(sname2)
        if (intsname1 < intsname2):
            line2 = url[0][0]
            Qs = line2.split("/")
            Line3 = url[1][0]
            Qd = Line3.split("/")
        else:
            line2 = url[1][0]
            Qs = line2.split("/")
            Line3 = url[0][0]
            Qd = Line3.split("/")
        # words = line2.split("/")
        Qsource = Qs[4]
        Qdestination = Qd[4]
        source.append(Qsource)
        destination.append(Qdestination)
    merg = {"Qsource": destination, "Qdestination": source}
    return merg




get_merge(newdf)



merg_export = pd.DataFrame(get_merge(newdf))
merg_export.to_excel("merg_export.xlsx")






