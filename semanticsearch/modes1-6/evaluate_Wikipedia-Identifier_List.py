import json
import dpath_util as dpath

path = "Wikipedia-Identifier_List.json"

with open(path,"r") as f:
    identifier_list = json.load(f)

# SORT CATALOGS TO GET RANKED LISTS

identifier_semantics_catalog = {}
semantics_identifier_catalog = {}

# get catalogs
for identifier in identifier_list.items():
    for semantics in identifier[1]:
        # extend identifier_semantics_catalog
        try:
            dpath.new(identifier_semantics_catalog,
                      identifier[0]
                      + "/" + semantics['description']
                      + "/" + semantics['value'],
                  None)
        except:
            print("Error processing " + semantics['identifier'] + "/" + semantics['description'])
        # extend semantics_identifier_catalog
        try:
            dpath.new(semantics_identifier_catalog,
                      semantics['description']
                      + "/" + identifier[0]
                      + "/" + semantics['value'],
                  None)
        except:
            print("Error processing " + semantics['description'] + "/" + semantics['identifier'])

# sort catalogs
for identifier in identifier_semantics_catalog.items():
    tmp_identifier = {}
    for semantics in identifier[1].items():
        for score in semantics[1]:
            try:
                tmp_identifier[semantics[0]] = float(score)
            except:
                print(score)
    identifier_semantics_catalog[identifier[0]] = {k:v for k, v in sorted(tmp_identifier.items(), key=lambda item: item[1],reverse=True)}
for semantics in semantics_identifier_catalog.items():
    tmp_semantics = {}
    for identifier in semantics[1].items():
        for score in identifier[1]:
            try:
                tmp_semantics[identifier[0]] = float(score)
            except:
                print(score)
    semantics_identifier_catalog[semantics[0]] = {k:v for k, v in sorted(tmp_semantics.items(), key=lambda item: item[1],reverse=True)}

# save catalogs
with open('Wikipedia_identifier_semantics_catalog.json', 'w', encoding='utf8') as f:
    json.dump(identifier_semantics_catalog,f)
with open('Wikipedia_semantics_identifier_catalog.json', 'w', encoding='utf8') as f:
    json.dump(semantics_identifier_catalog,f)

# EVALUATE EXAMPLE QUERIES

# Load example queries
with open('../examples_list/formula_examples.json', 'r', encoding='utf8') as f:
    example_queries = json.load(f)

# Get results
results = {}
for example_query in example_queries:

    results[example_query['GoldID']] = {}
    results[example_query['GoldID']]['name'] = example_query['formula_name']
    results[example_query['GoldID']]['tex'] = example_query['formula_tex']

    identifier_symbols = example_query['identifier_symbols']
    identifier_names = example_query['identifier_names']

    # Find index results
    for identifier_symbol in identifier_symbols:
        try:
            results[example_query['GoldID']][identifier_symbol]\
                = identifier_semantics_catalog[identifier_symbol]
        except:
            pass
    for identifier_name in identifier_names:
        try:
            results[example_query['GoldID']][identifier_name]\
                = semantics_identifier_catalog[identifier_name]
        except:
            results[example_query['GoldID']][identifier_name] = {}

# Save results
with open('Wikipedia_index_candidates.json', 'w', encoding='utf8') as f:
    json.dump(results,f)

print("end")