import json

# Load example queries
with open('formula_examples.json', 'r', encoding='utf8') as f:
    example_queries = json.load(f)

csv_list = []
for example_query in example_queries:
    for name in example_query['identifier_names']:
        csv_list.append(name + "\n")
        #csv_list.append(example_query['GoldID'] + "\n")
    for symbol in example_query['identifier_symbols']:
        csv_list.append(symbol + "\n")
        #csv_list.append(example_query['GoldID'] + "\n")

with open("list_template.csv", 'w') as f:
    f.writelines(csv_list)