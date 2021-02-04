# Perform semantic search using and (inverse) semantic index
# on NTCIR arXiv (astro-ph) or Wikipedia (MathIR task) dataset respectively

#TODO include Formula Concept Database (AnnoMathTeX)

import json
import pickle

#root_path = "E:\\MathQa/semanticsearch/"
root_path = ""
subject = "astro-ph"
#subject = ""

# UTILE FUNCTIONS
# define function for dict list appending
def append_to_list_if_unique(list,item):
    if item not in list:
        list.append(item)

def append_to_dict_list(dict,key,item,unique):
    if key in dict:
        if unique:
            append_to_list_if_unique(dict[key],item)
        else:
            dict[key].append(item)
    else:
        dict[key] = []
        if unique:
            append_to_list_if_unique(dict[key],item)
        else:
            dict[key].append(item)

# OPEN CATALOGS
def get_formula_catalog(catalog):
    # open formula catalog
    catalog_filename = catalog + "-Formula_Catalog.pkl"

    with open(root_path + catalog_filename, "rb") as f:
        Formula_Catalog = pickle.load(f)
    return Formula_Catalog

def get_identifier_semantics_catalog(inverse,multiple):
    # get Wikipedia (inverse) identifier semantics catalog (single or multiple)
    if inverse:
        mode1 = "Inverse_"
    else:
        mode1 = ""
    if multiple:
        mode2 = "_multiple"
    else:
        mode2 = "_single"

    file_path = root_path + "Wikipedia-" + mode1 + "Identifier_Semantics_Catalog" + mode2 + ".pkl"

    with open(file_path, "rb") as f:
        Identifier_Semantics_Catalog = pickle.load(f)
    return Identifier_Semantics_Catalog

# FORMULA SEARCH
def search_formulae_by_identifier_symbols(identifier_symbols,catalog):

    # open catalogs
    Formula_Catalog = get_formula_catalog(catalog=catalog)

    # find all formulae containing at least one identifier symbol from all queried names
    query_results = {}
    for formula in Formula_Catalog.items():
        found = []
        for identifier_symbol in identifier_symbols:
            if identifier_symbol in formula[1]["id"]:
                    found.append(identifier_symbol)

        # add result if length of matching identifiers correct
        display_result = False
        if len(found) == len(identifier_symbols):
            # only if no other identifiers
            if exclusive_identifiers:
                if len(found) == len(formula[1]["id"]):
                    display_result = True
            else:
                display_result = True
        if display_result:
            query_results[formula[0] + " (" + formula[1]["file"] + ")"] = found

    # return query results
    return query_results

def search_formulae_by_identifier_names(identifier_names,catalog,multiple):

    # open catalogs
    Formula_Catalog = get_formula_catalog(catalog=catalog)
    Inverse_Identifier_Semantics_Catalog = get_identifier_semantics_catalog(inverse=True,multiple=multiple)

    # find all formulae containing at least one identifier symbol from all queried names
    query_results = {}
    for formula in Formula_Catalog.items():
        found = {}
        for identifier_name in identifier_names:
            try:
                identifierSymbols = Inverse_Identifier_Semantics_Catalog[identifier_name]
            except:
                identifierSymbols = []
            for identifierSymbol in identifierSymbols:
                if identifierSymbol in formula[1]["id"]:
                    append_to_dict_list(found,identifier_name,identifierSymbol,unique=True)

        # add result if length of matching identifiers correct
        display_result = False
        if len(found) == len(identifier_names):
            # only if no other identifiers
            if exclusive_identifiers:
                if len(found) == len(formula[1]["id"]):
                    display_result = True
            else:
                display_result = True
        if display_result:
            query_results[formula[0] + " (" + formula[1]["file"] + ")"] = found

    # return query results
    return query_results

# EVALUATION

def search_formulae_by_identifier(identifier_symbols,identifier_names,mode_number):

    catalogs = ["NTCIR-12_Wikipedia","NTCIR-12_arXiv" + "_" + subject]
    identifier_input_modes = ["symbols","names"]
    multiple_modes = [False,True]

    # 6 evaluation modes:
    # wikip,symbs,single if mode_number == 1
    # wikip,names,single if mode_number == 2
    # wikip,names,multiple if mode_number == 3
    # arxiv,symbs,single if mode_number == 4
    # arxiv,names,single if mode_number == 5
    # arxiv,names,multiple if mode_number == 6
    if mode_number == 1:
        mode_vector = [0,0,0]
    if mode_number == 2:
        mode_vector = [0,1,0]
    if mode_number == 3:
        mode_vector = [0,1,1]
    if mode_number == 4:
        mode_vector = [1,0,0]
    if mode_number == 5:
        mode_vector = [1,1,0]
    if mode_number == 6:
        mode_vector = [1,1,1]

    catalog=catalogs[mode_vector[0]]
    identifier_input_mode=identifier_input_modes[mode_vector[1]]
    multiple_mode=multiple_modes[mode_vector[2]]

    if identifier_input_mode == "symbols":
        query_results = \
            search_formulae_by_identifier_symbols(
            identifier_symbols=identifier_symbols,
            catalog=catalog
        )
    elif identifier_input_mode == "names":
        query_results = \
            search_formulae_by_identifier_names(
            identifier_names=identifier_names,
            catalog=catalog,
            multiple=multiple_mode
        )

    return query_results

# EXECUTION

# OPTIONS HERE!

exclusive_identifiers = True

query_results = {}

# query examples

#example_queries = get_examples()
with open('../examples_list/formula_examples.json', 'r', encoding='utf8') as f:
    example_queries = json.load(f)

# query mode numbers
mode_numbers = [1,2,3,4,5,6]

for example_query in example_queries:
    print(example_query)
    query_results[example_query['formula_name']] = {}
    for mode_number in mode_numbers:
        query_results[example_query['formula_name']][mode_number] = search_formulae_by_identifier(
            identifier_symbols=example_query['identifier_symbols'],
            identifier_names=example_query['identifier_names'],
            mode_number=mode_number)

# mode mapping
mode_mapping = {'1': '10', '2': '8', '3': '8', '4': '11', '5': '7', '6': '7'}

# create candidates table
csv_lines = []
csv_lines.append("Name \t Formula \t Mode(new) \t Mode(old) \t Identifiers \n")
for query_result in query_results.items():
    for mode in query_result[1].items():
        # display only first result for specific mode
        displayed = False
        for formula in mode[1].items():
            if True: #displayed == False:
                csv_lines.append(str(query_result[0]) + "\t"
                                 + str(formula[0]).replace("\t","").replace("\n","") + "\t"
                                 + str(mode_mapping[str(mode[0])]) + "\t" + str(mode[0])
                                 + "\t" + str(formula[1]) + "\n")
                displayed = True

with open("SemanticSearch_arXivWikipedia.csv",'w',encoding='utf8') as f:
    f.writelines(csv_lines)

print("end")