import json
import pickle

with open('arXiv-Identifier_Statistics.pkl', "rb") as f:
    identifier_list = pickle.load(f)

# SORT CATALOGS TO GET RANKED LISTS

identifier_semantics_catalog = {}
semantics_identifier_catalog = identifier_list['semantics_identifier_distribution']

for semantics in semantics_identifier_catalog.items():
    for identifier in semantics[1].items():
        # extent identifier_semantics_catalog
        try:
            identifier_semantics_catalog[identifier[0]][semantics[0]] = identifier[1]
        except:
            identifier_semantics_catalog[identifier[0]] = {}
            identifier_semantics_catalog[identifier[0]][semantics[0]] = identifier[1]

# sort catalogs
for identifier in identifier_semantics_catalog.items():
    identifier_semantics_catalog[identifier[0]] = {k:v for k, v in sorted(identifier[1].items(), key=lambda item: item[1],reverse=True)}
for semantics in semantics_identifier_catalog.items():
    semantics_identifier_catalog[semantics[0]] = {k:v for k, v in sorted(semantics[1].items(), key=lambda item: item[1],reverse=True)}

# save catalogs
with open('arXiv_identifier_semantics_catalog.json', 'w', encoding='utf8') as f:
    json.dump(identifier_semantics_catalog,f)
with open('arXiv_semantics_identifier_catalog.json', 'w', encoding='utf8') as f:
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
with open('arXiv_index_candidates.json', 'w', encoding='utf8') as f:
    json.dump(results,f)

print("end")