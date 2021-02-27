import json

arXiv_identifier_list_file = "semanticsearch/modes1-6/arXiv_semantics_identifier_catalog.json"
Wikipedia_identifier_list_file = "semanticsearch/modes1-6/Wikipedia_semantics_identifier_catalog.json"

def get_identifier_symbol(identifier_name):

    # load identifier catalog
    # Wikipedia is best performing
    with open(Wikipedia_identifier_list_file,"r") as f:
        identifier_catalog = json.load(f)

    identifier_symbols = list(identifier_catalog[identifier_name[0]])
    identifier_symbol = identifier_symbols[0]

    return identifier_symbol