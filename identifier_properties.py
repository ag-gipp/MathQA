import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON
import json

# example Wikidata formula QID and identifier search string
# formula = "Q11432"
# identifier = "R"

def retrieve_identifier_name(formula, identifier):

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""#find identifier name
        SELECT ?identifierLabel WHERE {
        wd:""" + formula + """ p:P527 ?statement. #p: points to statement node
        ?statement ps:P527 ?identifier. #ps: property statement
        ?statement pq:P2534 ?symbol. #ps: property qualifier
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        FILTER(CONTAINS(STR(?symbol), '<mi>""" + identifier + """</mi>'))
        }""")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        tmp_results = []
        for result in results["results"]["bindings"]:
            tmp_results.append(result)

        json_str = json.dumps(tmp_results[0])
        resp = json.loads(json_str)
        return resp['identifierLabel']['value']

    except:
        return ""
    
def retrieve_identifier_value(formula, identifier):

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""#find identifier value
        SELECT ?value WHERE {
        wd:""" + formula + """ wdt:P527 ?identifier.
        ?identifier wdt:P416 ?symbol.
        ?identifier wdt:P1181 ?value.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        FILTER(STR(?symbol) = '""" + identifier + """')
        }""")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        tmp_results = []
        for result in results["results"]["bindings"]:
            tmp_results.append(result)

        json_str = json.dumps(tmp_results[0])
        resp = json.loads(json_str)
        return resp['value']['value']

    except:
        return ""
