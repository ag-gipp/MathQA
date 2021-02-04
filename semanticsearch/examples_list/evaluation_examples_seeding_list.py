import os
import re
import json
import requests

path = "../mathmlben"

def get_name_of_item(QID):

    URL = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=%s&format=json"

    try:
        r = requests.get(URL % QID)
        item_name = r.json()['entities'][QID]['labels']['en']['value']
    except:
        item_name = 'N/A'

    return item_name

def get_examples():
    example_files = [os.path.join(path, f) for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))]
    examples = []
    for example_file in example_files:
        with open(example_file,'r',encoding='utf8') as f:
            example_json = json.load(f)

        example = {}
        example['GoldID'] = example_file[-8:-5]
        print(example['GoldID'])
        example['formula_name'] = example_json['title']
        example['formula_tex'] = example_json['correct_tex']

        # parse semantic tex to get identifier symbols and qids
        semantic_tex = example_json['math_inputtex_semantic']
        example['semantic_tex'] = semantic_tex
        # find strings between brackets '{}'
        contents = re.findall(r'\{.*?\}',semantic_tex)
        # get identifier names and symbols
        identifier_qids = []
        identifier_names = []
        identifier_symbols = []
        # START RETRIEVAL
        for content in contents:
            if 'Q' in content:
                qid = re.findall(r'Q.*?\}',content)[0].strip("}")
                name = get_name_of_item(qid)
                identifier_qids.append(qid)
                identifier_names.append(name)
            else:
                symbol = content[1:-1]
                identifier_symbols.append(symbol)
        # END RETRIEVAL
        example['identifier_symbols'] = identifier_symbols
        example['identifier_names'] = identifier_names
        example['identifier_qids'] = identifier_qids

        # append example to list
        examples.append(example)

    return examples

# EXECUTE

examples = get_examples()

# save dict
with open('formula_examples(old).json', 'w', encoding='utf8') as f:
    json.dump(examples,f)

# OLD EXAMPLES

# if example_number == 1:
#     identifier_symbols = ["E", "m", "c"]
#     identifier_names = ["energy", "mass", "speed of light"]
#
# if example_number == 2:
#     identifier_symbols = ["F", "m", "a"]
#     identifier_names = ["force", "mass", "acceleration"]
#
# if example_number == 3:
#     identifier_symbols = ["E", "m", "v"]
#     identifier_names = ["energy", "mass", "velocity"]
#
# if example_number == 4:
#     identifier_symbols = ["U", "m", "g", "h"]
#     identifier_names = ["energy", "mass", "acceleration", "height"]
#
# if example_number == 5:
#     identifier_symbols = ["E", "k", "x"]
#     identifier_names = ["energy", "spring", "displacement"]
#
# if example_number == 6:
#     identifier_symbols = ["a", "v", "t"]
#     identifier_names = ["acceleration", "velocity", "time"]
#
# if example_number == 7:
#     identifier_symbols = ["\\omega", "f"]
#     identifier_names = ["angular frequency", "frequency"]