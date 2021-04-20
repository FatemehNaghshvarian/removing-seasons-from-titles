import sys
from SPARQLWrapper import SPARQLWrapper, JSON
#import pandas as pd
import re

#Titles without the dates
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?item ?itemLabel 
WHERE {
  ?item wdt:P5935 ?id;
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,nl". }
}

"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

def get_production_label_without_date(results):
    productions = []
    for result in results["results"]["bindings"]:
        production = re.sub(r'\([^)]*\)', '', result["itemLabel"]["value"])
        productions.append(production)
    return productions

productions = get_production_label_without_date(results)

labels_without_dates =set((productions)) # this is the full set of productions that you get
#labels_without_dates = set(["label without date 1", "label without date 2", ...])  # this is simply the "set" of unique labels without dates that you get, see also https://www.w3schools.com/python/python_sets.asp; sets do not allow duplicate values
production_groups = {label: [] for label in labels_without_dates}  # this will become the dictionary in which you store the groups of productions, c.q. reruns; the key will be the label_without_date, the value will be an array of productions; I used dict comprehension here, see https://docs.python.org/3/tutorial/datastructures.html#dictionaries
for label in labels_without_dates:
    for production in productions:
        production_label_without_date = get_production_label_without_date(results)  # this is some function that gets the label of a production without season info, should be the same code that is used to make labels_without_dates
        if label == production_label_without_date:
            production_groups[label].append(production)

print(production_groups)