import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON
import json

#---------
#PYWIKIBOT
#---------

def retrieve_identifiers(formulaName)

    #retrieve Wikidata page item
    identifiers = dict()
    try:
        site = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(site, formulaName)
        item = pywikibot.ItemPage.fromPage(page)
        #formulaQID = str(item).replace("[[wikidata:", '').replace("]]", '')
        #formula_string = item.claims['P2534'][0].getTarget()

        #retrieve identifiers
        identifier_list = item.claims['P527']
        identifier_symbol = ""
        identifier_name = ""
        identifier_value = ""
        for identifier in identifier_list:

            identifier_symbol = str(identifier.qualifiers['P2534'][0].target)
            identifier_name = str(identifier.getTarget().text['labels']['en'])

            identifiers[identifier_symbol] = {}
            identifiers[identifier_symbol]['name'] = identifier_name
            try:
                identifier_value = str(identifier.getTarget().claims['P1181'][0].getTarget().amount)
                identifiers[identifier_symbol]['value'] = identifier_value
            except:
                pass
        return identifiers

    except:
        return dict()

#------
#SPARQL
#------

def retrieve_identifier_name(formulaQID, identifierSymbol):

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""#find identifier name
        SELECT ?identifierLabel WHERE {
        wd:""" + formulaQID + """ p:P527 ?statement. #p: points to statement node
        ?statement ps:P527 ?identifier. #ps: property statement
        ?statement pq:P2534 ?symbol. #ps: property qualifier
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        FILTER(CONTAINS(STR(?symbol), '<mi>""" + identifierSymbol + """</mi>'))
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
    
def retrieve_identifier_value(formulaQID, identifierSymbol):

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""#find identifier value
        SELECT ?value WHERE {
        wd:""" + formulaQID + """ wdt:P527 ?identifier.
        ?identifier wdt:P416 ?symbol.
        ?identifier wdt:P1181 ?value.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        FILTER(STR(?symbol) = '""" + identifierSymbol + """')
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