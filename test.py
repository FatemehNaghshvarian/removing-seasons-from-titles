# This one contains the reruns as well.
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
# import pandas as pd
import re
from json import dumps

# Titles without the dates
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?item ?itemLabel 
WHERE {
  ?item wdt:P5935 ?id;
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,nl". }
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
    production = re.sub(r'\([^)]*\)', '', result["itemLabel"]["value"])
    production = production.strip() if production.strip() != "" else None
    return production


productions = [get_production_label_without_date(result) for result in results["results"]["bindings"]]

labels_without_dates = set((productions))  # this is the full set of productions that you get
production_groups = {label: [] for label in
                     labels_without_dates}  # this will become the dictionary in which you store the groups of productions, c.q. reruns; the key will be the label_without_date, the value will be an array of productions; I used dict comprehension here, see https://docs.python.org/3/tutorial/datastructures.html#dictionaries
for label in labels_without_dates:
    for result in results["results"]["bindings"]:
        production_label_without_date = get_production_label_without_date(
            result)  # this is some function that gets the label of a production without season info, should be the same code that is used to make labels_without_dates
        if label == production_label_without_date:
            production_groups[label].append((production_label_without_date))

print(dumps(production_groups, indent=2))

#for production in production_groups[label]:
query = """SELECT ?item ?label
WHERE {
  ?item wdt:P5935 ?id;
        rdfs:label ?label.
  # FILTER(LANG(?label) = "nl").  
  FILTER(STRSTARTS(?label, "Augustus")).
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl,en". }
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

for result in results["results"]["bindings"]:
    print(result)


