import json

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

# Load example queries
with open('../examples_list/formula_examples.json', 'r', encoding='utf8') as f:
    example_queries = json.load(f)

results = {}
for example_query in example_queries:
    GoldID = example_query['GoldID']
    FormulaName = example_query['formula_name']
    # retrieve only results that are common in all query word results
    common_results = {}
    for query_word in FormulaName.split():
        try:
            for formula in formula_index[query_word].items():
                try:
                    common_results[formula[0]] += 1
                except:
                    common_results[formula[0]] = 1
        except:
            pass
    ranking = {}
    for common_result in common_results.items():
        if True: #common_result[1] == len(FormulaName.split()):
            for query_word in FormulaName.split():
                try:
                    ranking[common_result[0]] += formula_index[query_word][common_result[0]]
                except:
                    try:
                        ranking[common_result[0]] = formula_index[query_word][common_result[0]]
                    except:
                        pass

    result = {k: v for k, v in sorted(ranking.items(), key=lambda item: item[1],reverse=True)}
    results[GoldID] = (FormulaName,result)

# output to csv
csv_list = []
csv_list.append("GoldID\tName\tFormula\t(Score,Rank)\tDCG\tnDCG\n")
for result in results.items():
    # display only first hits or ranking cutoff
    displayed = False
    counter = 0
    for formula in result[1][1].items():
        if counter < 10: # True: #displayed == False:
            csv_list.append(result[0] + "\t" + result[1][0] + "\t"
                            + formula[0].replace("\t","").replace("\n","") + "\t\t\t\n")
            displayed = True
            counter += 1

with open("inverse_formula_index_results.csv", 'w', encoding='utf8') as f:
    f.writelines(csv_list)

print("end")