import json
import SPARQLWrapper
import pywikibot

# Define functions

def get_sparql_results(sparql_query_string):
    sparql = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query_string)
    try:
        # stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
        result = sparql.query()
        sparql.setReturnFormat(SPARQLWrapper.JSON)
        result = sparql.query().convert()
    except:
        result = None
    return result

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

def get_sparql_string_identifier_symbols(contains_line):
    sparql_query = """#find items with defining formula containing identifier symbols
    SELECT ?item ?itemLabel ?formula WHERE {
      ?item wdt:P2534 ?formula.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
      FILTER(%s)
    }""" % contains_line.strip(" && ")
    return sparql_query

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

def get_sparql_query_identifier_names(identifier_names_list):
    # compile sparql query

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
    print(sparql_query_has_part)
    print(sparql_query_calculated_from)

    return get_sparql_results(sparql_query_has_part),\
           get_sparql_results(sparql_query_calculated_from)

def get_sparql_query_identifier_qids(identifier_qid_list):
    # compile sparql query

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
    print(sparql_query_has_part)
    print(sparql_query_calculated_from)

    return get_sparql_results(sparql_query_has_part),\
           get_sparql_results(sparql_query_calculated_from)

def get_sparql_query_identifier_symbols(identifier_symbols_list):
    # compile sparql query

    # get contains query lines
    contains_line = ""
    calculated_from_lines = ""
    for identifier_symbol in identifier_symbols_list:
        contains_line += "CONTAINS(STR(?formula), '<mi>"\
                         + identifier_symbol + "</mi>') && "

    # get sparql queries
    sparql_query_symbols = get_sparql_string_identifier_symbols(contains_line)

    return get_sparql_results(sparql_query_symbols)

# Open examples
with open('formula_examples.json', 'r', encoding='utf8') as f:
    example_queries = json.load(f)

# Get results
# results = {}
# for example_query in example_queries:
#     # Evaluation Mode 9
#     # [1:] to discard left-hand side identifier
#     #results[example_query['formula_name']] \
#     #    = get_sparql_query_identifier_qids(example_query['identifier_qids'][1:])
#     #results[example_query['formula_name']]\
#     #    = get_sparql_query_identifier_names(example_query['identifier_names'][1:])
#     # Evaluation Mode 12
#     results[example_query['formula_name']]\
#         = get_sparql_query_identifier_symbols(example_query['identifier_symbols'][1:])
#     print()

#Mode9 or Mode12
#with open("SemanticSearch_WikidataMode12_allhits.json",'w',encoding='utf8') as f:
#    json.dump(results,f)
with open("SemanticSearch_WikidataMode12_allhits.json",'r',encoding='utf8') as f:
    results = json.load(f)

# Save results
csv_lines = []
csv_lines.append("Name \t Score \t Formula \n")
for result in results.items():
    if result[1] is not None:
        # Mode 9
        #for part_mode in result[1]:
            # try:
            #     for hit in part_mode['results']['bindings']:
        # Mode 12
        for hit in result[1]['results']['bindings']:
            #identifier = hit['partsLabel']['value']
            mathml = str(hit['formula']['value'])
            formula = (mathml.split('alttext="{'))[1].split('}">')[0]
            csv_line = result[0] + " \t 0 \t " + formula + " \n"
            # add to list discarding duplicates
            if csv_lines[-1] != csv_line:
                csv_lines.append(csv_line)
            #except:
            #    pass

#Mode9 or Mode12
with open("SemanticSearch_WikidataMode12_allhits.csv",'w',encoding='utf8') as f:
    f.writelines(csv_lines)

print("end")