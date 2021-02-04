# Build formula catalog and (inverse) semantic index
# from NTCIR arXiv (astro-ph) or Wikipedia (MathIR task) dataset respectively

#TODO include Formula Concept Database (AnnoMathTeX)

import os
#from bs4 import BeautifulSoup
import pickle
import json
import re

#root_path = ""
root_path = "../"

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

def most_frequent(list):
    return max(set(list), key = list.count)

# (INVERSE) IDENTIFIER SEMANTICS CATALOG
def create_identifier_semantics_catalog(mode):

    # open Wikipedia identifier list (Moritz)
    with open("../modes1-6/Wikipedia-Identifier_List.json", "r") as f:
        Identifier_List = json.load(f)

    # create (inverse) identifier annotation index
    Identifier_Semantics_Catalog = {}
    Inverse_Identifier_Semantics_Catalog = {}

    # only Latin and Greek letters are valid
    with open("../Latin_and_Greek_alphabet.txt", "r") as f:
        letters = [line.strip() for line in f]
    # iterate identifiers
    for identifier in Identifier_List.items():
        # get identifier string
        identifierString = identifier[0]
        # find valid alphabet characters
        symbols = []
        for letter in letters:
            if letter in identifierString:
                symbols.append(letter)
        # only the first symbol is the identifier (the others may be sub- oder superscripts)
        try:
            identifierSymbol = symbols[0]
            #print(identifierSymbol)

            # list descriptions/annotations
            descriptions = []
            for instance in identifier[1]:
                descriptions.append(instance["description"])

            # extent semantic index
            for description in descriptions:
                append_to_dict_list(Identifier_Semantics_Catalog, identifierSymbol, description, unique=False)
                append_to_dict_list(Inverse_Identifier_Semantics_Catalog,description,identifierSymbol,unique=False)

        except:
            pass

    # keep only the most frequent identifier symbol (_single)
    if mode == "single":
        for identifier_symbol in Identifier_Semantics_Catalog.items():
           Identifier_Semantics_Catalog[identifier_symbol[0]] = most_frequent(Identifier_Semantics_Catalog[identifier_symbol[0]])
        for identifier_name in Inverse_Identifier_Semantics_Catalog.items():
          Inverse_Identifier_Semantics_Catalog[identifier_name[0]] = most_frequent(Inverse_Identifier_Semantics_Catalog[identifier_name[0]])

    # remove duplicates (_multiple)
    elif mode == "multiple":
        for identifier_name in Identifier_Semantics_Catalog.items():
            Identifier_Semantics_Catalog[identifier_name[0]] = list(
                set(Identifier_Semantics_Catalog[identifier_name[0]]))
        for identifier_name in Inverse_Identifier_Semantics_Catalog.items():
            Inverse_Identifier_Semantics_Catalog[identifier_name[0]] = list(
                set(Inverse_Identifier_Semantics_Catalog[identifier_name[0]]))

    # save semantic index
    with open("Wikipedia-Identifier_Semantics_Catalog_" + mode + ".pkl", "wb") as f:
        pickle.dump(Identifier_Semantics_Catalog, f)
    with open("Wikipedia-Inverse_Identifier_Semantics_Catalog_" + mode + ".pkl", "wb") as f:
        pickle.dump(Inverse_Identifier_Semantics_Catalog,f)

# FORMULA CATALOG
def create_formula_catalog(dataset):

    if dataset == "NTCIR-12_Wikipedia":
        dataset_filepiece = "NTCIR-12_Wikipedia"
        file_ending = "html"
        formula_tag = "math"
        identifier_tag = "mi"
    if dataset == "NTCIR-12_arXiv_astro-ph":
        dataset_filepiece = "NTCIR-12_arXiv_astro-ph"
        file_ending = "tei"
        formula_tag = "formula"
        identifier_tag = "m:mi"
    if dataset == "NTCIR-12_arXiv":
        dataset_filepiece = "NTCIR-12_arXiv"
        file_ending = "tei"
        formula_tag = "formula"
        identifier_tag = "m:mi"

    Formula_Catalog = {}

    file_counter = 0

    for file in os.listdir(root_path):
        if file.endswith(file_ending):# and file_counter < 25:
            print(file)
            file_counter += 1
            print(file_counter)
            with open("" + file,"r",encoding="utf8") as f:
                text = f.read()
                soup = BeautifulSoup(text)#,features="lxml")

                formulae = soup.find_all(formula_tag)
                for formula in formulae:

                    try:
                        # get and soupify formula string
                        formulaString = str(formula.contents)
                        soup = BeautifulSoup(formulaString)

                        # get formulaTeX string
                        if dataset == "NTCIR-12_Wikipedia":
                            s = formulaString
                            start = 'alttext="'
                            end = '" display='
                            formulaTeXString = re.search('%s(.*)%s' % (start, end), s).group(1)

                        if dataset == "NTCIR-12_arXiv_astro-ph":
                            formulaTeXString = soup.find_all("annotation")
                            # strip off newline chars (from left and right)
                            formulaTeXString = str(formulaTeXString[0].contents[0]).strip()

                        # create formula catalog entry
                        Formula_Catalog[formulaTeXString] = {}

                        # add filename
                        Formula_Catalog[formulaTeXString]["file"] = file

                        # create identifier list
                        Formula_Catalog[formulaTeXString]["id"] = []

                        # retrieve identifiers
                        identifiers = soup.find_all(identifier_tag)
                        for identifier in identifiers:
                            try:
                                identifier = str(identifier.contents[0])
                                Formula_Catalog[formulaTeXString]["id"].append(identifier)
                            except:
                                pass

                        # remove formula if no equation or without identifiers
                        if len(Formula_Catalog[formulaTeXString]["id"]) == 0 or not "=" in formulaTeXString:
                            del Formula_Catalog[formulaTeXString]
                        else:
                            # remove duplicate identifiers
                            Formula_Catalog[formulaTeXString]["id"] = list(set(Formula_Catalog[formulaTeXString]["id"]))

                    except:
                        pass

    # save formula catalog
    with open(dataset_filepiece + "-Formula_Catalog.pkl", "wb") as f:
        pickle.dump(Formula_Catalog,f)

def convert_formula_catalog(input_path,dataset_name):

    # open formula catalog to be converted
    with open(input_path,"rb") as f:
        catalog = pickle.load(f)

    # init converted formula catalog
    Formula_Catalog = {}

    # get rid of operator and identifier catalog
    del catalog['operator_catalog']
    del catalog['identifier_catalog']

    # left with list of formulae
    total = len(catalog)
    counter = 0
    for formula in catalog.items():
        try:
            Formula_Catalog[formula[1]['TeX']] = {}
            Formula_Catalog[formula[1]['TeX']]['file'] = formula[1]['filename']
            Formula_Catalog[formula[1]['TeX']]['id'] = list()
            for identifier in formula[1]['identifiers'].items():
                Formula_Catalog[formula[1]['TeX']]['id'].append(identifier[1])
        except:
            pass
        counter += 1
        print("Processed formula " + str(counter) + "/" + str(total))

    # save formula catalog
    with open("E:\\MathQa/semanticsearch/" + dataset_name + "-Formula_Catalog.pkl", "wb") as f:
        pickle.dump(Formula_Catalog, f)

# EXECUTIONS

create_identifier_semantics_catalog(mode="single")#mode="multiple
#create_formula_catalog(dataset="NTCIR-12_arXiv")#dataset="NTCIR-12_arXiv_astro-ph", dataset="NTCIR-12_Wikipedia"
#convert_formula_catalog(input_path="E:\\NTCIR-12_MathIR_arXiv_Corpus/output_FeatAna/formula_catalog.pkl",dataset_name="NTCIR-12_arXiv")

print("end")