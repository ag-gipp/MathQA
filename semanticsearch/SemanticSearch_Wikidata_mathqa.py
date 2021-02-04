import SPARQLWrapper
import pywikibot

# Define functions

# get identifier qid from name using pywikibot
def get_identifier_qid(identifier_name):
    try:
        site = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(site, identifier_name)
        item = pywikibot.ItemPage.fromPage(page)
        qid = item.id
    except:
        qid = None
    return qid

# get sparql query for Wikidata 'has part' or 'calculated from' properties
def get_sparql_string_identifier_qids(part_lines):
    sparql_query = """# Find items with 'has part' or 'calculated from' QIDs
    SELECT ?item ?itemLabel ?formula ?parts ?partsLabel WHERE {
        %s
        ?item wdt:P2534 ?formula.
        SERVICE wikibase:label {
        bd:serviceParam wikibase:language "en" .
        }
    }""" % part_lines
    return sparql_query

# get sparql query for identifier symbols in mathml string
def get_sparql_string_identifier_symbols(contains_line):
    sparql_query = """#find items with defining formula containing identifier symbols
    SELECT ?item ?itemLabel ?formula WHERE {
      ?item wdt:P2534 ?formula.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
      FILTER(%s)
    }""" % contains_line.strip(" && ")
    return sparql_query

# get sparql results for sparql query string
def get_sparql_results(sparql_query_string):
    sparql = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query_string)
    try:
        # stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
        sparql.setReturnFormat(SPARQLWrapper.JSON)
        result = sparql.query().convert()
    except:
        result = None
    return result

# get formulae using identifier names
def get_sparql_query_results_identifier_names(identifier_names_list):

    # get part query lines
    has_part_lines = ""
    calculated_from_lines = ""
    for identifier_name in identifier_names_list:
        identifier_qid = get_identifier_qid(identifier_name)
        if identifier_qid is not None:
            # 'has part' (P527) query lines
            has_part_lines += "\t?item wdt:P527 wd:" + identifier_qid + ".\n"
            # 'calculated from' (P4934) query lines
            calculated_from_lines += "\t?item wdt:P4934 wd:" + identifier_qid + ".\n"
    has_part_lines += "?item wdt:P527 ?parts.\n"
    calculated_from_lines += "?item wdt:P4934 ?parts.\n"

    # get sparql queries
    sparql_query_has_part = get_sparql_string_identifier_qids(has_part_lines)
    sparql_query_calculated_from = get_sparql_string_identifier_qids(calculated_from_lines)

    return get_sparql_results(sparql_query_has_part),\
           get_sparql_results(sparql_query_calculated_from)

# get formulae using identifier qids
def get_sparql_query_results_identifier_qids(identifier_qid_list):

    # get part query lines
    has_part_lines = ""
    calculated_from_lines = ""
    for identifier_qid in identifier_qid_list:
        if identifier_qid is not None:
            # 'has part' (P527) query lines
            has_part_lines += "\t?item wdt:P527 wd:" + identifier_qid + ".\n"
            # 'calculated from' (P4934) query lines
            calculated_from_lines += "\t?item wdt:P4934 wd:" + identifier_qid + ".\n"
    has_part_lines += "?item wdt:P527 ?parts.\n"
    calculated_from_lines += "?item wdt:P4934 ?parts.\n"

    # get sparql queries
    sparql_query_has_part = get_sparql_string_identifier_qids(has_part_lines)
    sparql_query_calculated_from = get_sparql_string_identifier_qids(calculated_from_lines)

    return get_sparql_results(sparql_query_has_part),\
           get_sparql_results(sparql_query_calculated_from)

# get formulae using identifier symbols
def get_sparql_query_results_identifier_symbols(identifier_symbols_list):

    # get contains query lines
    contains_line = ""
    calculated_from_lines = ""
    for identifier_symbol in identifier_symbols_list:
        contains_line += "CONTAINS(STR(?formula), '<mi>"\
                         + identifier_symbol + "</mi>') && "

    # get sparql queries
    sparql_query_symbols = get_sparql_string_identifier_symbols(contains_line)

    return get_sparql_results(sparql_query_symbols)

def search_formulae_by_identifiers_Wikidata(identifier_names):

    sparql_results = get_sparql_query_results_identifier_names(identifier_names)

    first_hit = sparql_results[0]['results']['bindings'][0]
    qid = first_hit['item']['value'].split("/")[-1]
    mathml = first_hit['formula']['value']
    formula = (mathml.split('alttext="{'))[1].split('}">')[0]
    identifiers = first_hit['partsLabel']['value']

    return {formula: [identifiers]}