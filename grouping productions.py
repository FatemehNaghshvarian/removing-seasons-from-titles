import sys
from SPARQLWrapper import SPARQLWrapper, JSON
#import pandas as pd
import re
from json import dumps

#Titles without the dates
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?item ?itemLabel 
WHERE {
  ?item wdt:P5935 ?id;
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
}
LIMIT 1000
"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

def get_production_label_without_date(result):
    season_regex = re.compile(r'\(\d{4}-\d{4}\)')
    season = season_regex.findall(result["itemLabel"]["value"]).pop()
    begin_year = int(season.split("-")[0][1:])
    end_year = int(season.split("-")[-1][:-1])
    production = re.sub(r'\([^)]*\)', '', result["itemLabel"]["value"])
    production = production.strip() if production.strip() != "" else None
    return (production, begin_year, end_year)

productions_seasons = [get_production_label_without_date(result) for result in results["results"]["bindings"]]

labels_without_dates = set([ps[0] for ps in productions_seasons]) # this is the full set of productions that you get
production_groups = {label: {"entities": [], "years": set()} for label in labels_without_dates}  # this will become the dictionary in which you store the groups of productions, c.q. reruns; the key will be the label_without_date, the value will be an array of productions; I used dict comprehension here, see https://docs.python.org/3/tutorial/datastructures.html#dictionaries
for label in labels_without_dates:
    for result in results["results"]["bindings"]:
        production_label_without_date, begin_year, end_year = get_production_label_without_date(result)  # this is some function that gets the label of a production without season info, should be the same code that is used to make labels_without_dates
        if label == production_label_without_date:
            production_groups[label]["entities"].append((result["item"]["value"], result["itemLabel"]["value"]))
            production_groups[label]["years"].add(begin_year)
            production_groups[label]["years"].add(end_year)

for production_group in production_groups:
    production = production_groups[production_group]
    if len(production["years"]) > 2:  # consider only productions with reruns
        print(production_group)
        print("\t", production["entities"])
        print("\tfrom", min(production["years"]), "until", max(production["years"]))


