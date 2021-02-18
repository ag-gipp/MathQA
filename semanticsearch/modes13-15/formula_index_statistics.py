import json
import numpy as np

# Set file paths
basePath = 'D:\\NTCIR-12_MathIR_arXiv_Corpus\\'
inputPath = basePath + "output_FeatAna\\"
index_file = 'inverse_semantic_index_formula_catalog(physics_all).json'
#basePath = 'D:\\NTCIR-12_MathIR_Wikipedia_Corpus\\'
#inputPath = basePath + "output_RE\\"
#index_file = 'inverse_semantic_index_formula_catalog(Wikipedia).json'

# Load inverse index
with open(inputPath + index_file,'r',encoding='utf8') as f:
    formula_index = json.load(f)

# retrieve numbers to calculate average/total number of formulae
numbers = []
for entry in formula_index.items():
    numbers.append(len(entry[1]))

# get avg / tot nr.
print("Average: " + str(np.mean(numbers)))
print("Total: " + str(sum(numbers)))

print("end")