import json
import SPARQLWrapper

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

sparql_query_string = """select * where {
  {
  ?item wdt:P416 ?symbol .
  filter exists { ?item wdt:P416 [] . }
  optional { ?item rdfs:label ?label.
            filter (lang(?label) = "en") }
    }
  UNION
  {
  ?item wdt:P7973 ?symbol .
  filter exists { ?item wdt:P7973 [] . }
  optional { ?item rdfs:label ?label.
            filter (lang(?label) = "en") }
    }
  UNION
  {
  ?item wdt:P7235 ?symbol .
  filter exists { ?item wdt:P7235 [] . }
  optional { ?item rdfs:label ?label.
            filter (lang(?label) = "en") }
    }
}"""

results = get_sparql_results(sparql_query_string)

# create semantic index
semantics_identifier_catalog = {}
identifier_semantics_catalog = {}
for result in results['results']['bindings']:
    try:
        name = result['label']['value']
        symbol = result['symbol']['value'][0]# only first letter, no indices
    except:
        pass
    # expand semantics_identifier_catalog
    try:
        semantics_identifier_catalog[name][symbol] += 1
    except:
        try:
            semantics_identifier_catalog[name][symbol] = 1
        except:
            semantics_identifier_catalog[name] = {}
            semantics_identifier_catalog[name][symbol] = 1
    # expand identifier_semantics_catalog
    try:
        identifier_semantics_catalog[symbol][name] += 1
    except:
        try:
            identifier_semantics_catalog[symbol][name] = 1
        except:
            identifier_semantics_catalog[symbol] = {}
            identifier_semantics_catalog[symbol][name] = 1

# Load example queries
with open('../examples_list/formula_examples.json', 'r', encoding='utf8') as f:
    example_queries = json.load(f)

# Get and save results
semantics_identifiers = ["Name\tCandidates\n"]
identifiers_semantics = ["Symbol\tCandidates\n"]
scores = {}
for example_query in example_queries:
    example = example_query['formula_name']
    scores[example] = {}
    names = example_query['identifier_names']
    symbols = example_query['identifier_symbols']
    for name in names:
        try:
            scores[example][name] = semantics_identifier_catalog[name]
            semantics_identifiers.append(name + "\t" + str(semantics_identifier_catalog[name]) + "\n")
        except:
            scores[example][name] = None
    for symbol in symbols:
        try:
            scores[example][symbol] = identifier_semantics_catalog[symbol]
            identifiers_semantics.append(symbol + "\t" + str(identifier_semantics_catalog[symbol]) + "\n")
        except:
            scores[example][symbol] = None

with open("NamesToSymbols_Wikidata.csv",'w',encoding='utf8') as f:
    f.writelines(semantics_identifiers)
with open("SymbolsToNames_Wikidata.csv",'w',encoding='utf8') as f:
    f.writelines(identifiers_semantics)

print("end")