import json
import numpy as np

# Set file paths
#index_file = "arXiv_identifier_semantics_catalog.json"
#index_file = "arXiv_semantics_identifier_catalog.json"
#index_file = "Wikipedia_identifier_semantics_catalog.json"
index_file = "Wikipedia_semantics_identifier_catalog.json"

# Load index
with open(index_file,'r',encoding='utf8') as f:
    identifier_index = json.load(f)

# retrieve numbers to calculate average/total number of formulae
numbers = []
for entry in identifier_index.items():
    numbers.append(len(entry[1]))

# get avg / tot nr.
print("Average: " + str(np.mean(numbers)))
print("Total: " + str(sum(numbers)))

print("end")