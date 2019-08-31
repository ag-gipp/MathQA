# Identifier relationship extraction

import os
from bs4 import BeautifulSoup
import pickle
import json

#filepath = ""
filepath = "semanticsearch/"

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

# OPEN CATALOGS
def get_formula_catalog():
    # open formula catalog
    with open(filepath + "NTCIR-12_Wikipedia-Formula_Catalog.pkl", "rb") as f:
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

    file_path = filepath + "Wikipedia-" + mode1 + "Identifier_Semantics_Catalog" + mode2 + ".pkl"

    with open(file_path, "rb") as f:
        Identifier_Semantics_Catalog = pickle.load(f)
    return Identifier_Semantics_Catalog

# FORMULA SEARCH
def search_formulae_by_identifier_symbols(identifier_symbols):

    # open catalogs
    Formula_Catalog = get_formula_catalog()

    # find all formulae containing at least one identifier symbol from all queried names
    query_results = {}
    for formula in Formula_Catalog.items():
        found = []
        for identifier_symbol in identifier_symbols:
            if identifier_symbol in formula[1]["id"]:
                    found.append(identifier_symbol)

        if len(found) == len(identifier_symbols):
            query_results[formula[0] + " (" + formula[1]["file"] + ")"] = found

    # return query results
    return query_results

def search_formulae_by_identifier_names(identifier_names):

    # open catalogs
    Formula_Catalog = get_formula_catalog()
    Inverse_Identifier_Semantics_Catalog = get_identifier_semantics_catalog(inverse=True,multiple=False)

    # find all formulae containing at least one identifier symbol from all queried names
    query_results = {}
    for formula in Formula_Catalog.items():
        found = {}
        for identifier_name in identifier_names:
            identifierSymbols = Inverse_Identifier_Semantics_Catalog[identifier_name]
            for identifierSymbol in identifierSymbols:
                if identifierSymbol in formula[1]["id"]:
                    append_to_dict_list(found,identifier_name,identifierSymbol,unique=True)

        if len(found) == len(identifier_names):
            query_results[formula[0] + " (" + formula[1]["file"] + ")"] = found

    # return query results
    return query_results

# IDENTIFIER SEMANTICS CATALOG
def create_identifier_semantics_catalog():

    # open Wikipedia identifier list (Moritz)
    with open("Wikipedia-Identifier_List.json", "r") as f:
        Identifier_List = json.load(f)

    # create (inverse) identifier annotation index
    Identifier_Semantics_Catalog = {}
    Inverse_Identifier_Semantics_Catalog = {}

    # only Latin and Greek letters are valid
    with open("Latin_and_Greek_alphabet.txt","r") as f:
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
    for identifier_symbol in Identifier_Semantics_Catalog.items():
        Identifier_Semantics_Catalog[identifier_symbol[0]] = most_frequent(Identifier_Semantics_Catalog[identifier_symbol[0]])
    for identifier_name in Inverse_Identifier_Semantics_Catalog.items():
       Inverse_Identifier_Semantics_Catalog[identifier_name[0]] = most_frequent(Inverse_Identifier_Semantics_Catalog[identifier_name[0]])

    # remove duplicates (_multiple)
    # for identifier_name in Identifier_Semantics_Catalog.items():
    #     Identifier_Semantics_Catalog[identifier_name[0]] = list(
    #         set(Identifier_Semantics_Catalog[identifier_name[0]]))
    # for identifier_name in Inverse_Identifier_Semantics_Catalog.items():
    #     Inverse_Identifier_Semantics_Catalog[identifier_name[0]] = list(
    #         set(Inverse_Identifier_Semantics_Catalog[identifier_name[0]]))

    # save semantic index
    with open("Wikipedia-Identifier_Semantics_Catalog_single.pkl", "wb") as f:
        pickle.dump(Identifier_Semantics_Catalog,f)
    #with open("Wikipedia-Identifier_Semantics_Catalog_multiple.pkl", "wb") as f:
        #pickle.dump(Identifier_Semantics_Catalog, f)
    with open("Wikipedia-Inverse_Identifier_Semantics_Catalog_single.pkl", "wb") as f:
        pickle.dump(Inverse_Identifier_Semantics_Catalog, f)
    #with open("Wikipedia-Inverse_Identifier_Semantics_Catalog_multiple.pkl", "wb") as f:
        #pickle.dump(Inverse_Identifier_Semantics_Catalog,f)

# FORMULA CATALOG
def create_formula_catalog():

    Formula_Catalog = {}

    file_counter = 0

    for file in os.listdir(filepath):
        if file.endswith("html"):# and file_counter < 25:
            print(file)
            file_counter += 1
            print(file_counter)
            with open("" + file,"r",encoding="utf8") as f:
                text = f.read()
                soup = BeautifulSoup(text)#,features="lxml")

                formulae = soup.find_all("math")
                for formula in formulae:

                    try:
                        # get and soupify formula string
                        formulaString = str(formula.contents)
                        soup = BeautifulSoup(formulaString)

                        # get formulaTeX string
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
                        identifiers = soup.find_all("mi")
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
    with open("NTCIR-12_Wikipedia-Formula_Catalog.pkl", "wb") as f:
        pickle.dump(Formula_Catalog,f)

# EXECUTIONS

#formula_catalog = get_formula_catalog()
#identifier_semantics_catalog = get_identifier_semantics_catalog(inverse=False,multiple=True)

#create_formula_catalog()
#create_identifier_semantics_catalog()

#query_result = search_formulae_by_identifier_names(["mass","energy","speed of light"])
#query_result = search_formulae_by_identifier_symbols(["m","E","c"])

#print("end")