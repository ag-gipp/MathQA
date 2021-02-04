from os import listdir
import json
from bs4 import BeautifulSoup

# Set file paths
basePath = 'D:\\NTCIR-12_MathIR_arXiv_Corpus\\'

datasetPath = basePath + "NTCIR12\\"
#valid_folder_prefix = ["0001"]
#valid_folder_prefix = ["00", "01", "02", "03", "04", "05", "06"]
#valid_folder_prefix = ["00", "01"]
valid_folder_prefix = [""]

outputPath = basePath + "output_FeatAna\\"

# Create inverse_semantic_index_formula_catalog
formula_index = {}

# Define class counter and desired classes
classCounter = {}
#classLimit = 100
#desired_classes = ['astro-ph']
desired_classes = ['astro-ph', 'cond-mat', 'gr-qc', 'hep-lat', 'hep-ph', 'hep-th', 'math-ph', 'nlin', 'quant-ph', 'physics']

# exclude formulae, stopwords, html and letters from candidates
excluded = [">", "<", "=", "~",'"', "_"]
with open("../stopwords.txt") as f:
    stopwords = [line.strip() for line in f]
#invalid = ["times"]
with open("../letters.txt") as f:
    letters = [line.strip() for line in f]

def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)

# Fetch content and labels of documents
for Dir in listdir(datasetPath):
    for prefix in valid_folder_prefix:
        if Dir.startswith(prefix):
            for File in listdir(datasetPath + "\\" + Dir):
                if not File.startswith("1") and File.endswith(".tei"):
                    # fetch label from file prefix
                    if Dir.startswith("9"):
                        classLab = File.split("9")[0]
                    else:
                        classLab = File.split("0")[0]
                    # check if class is desired and limit is not exceeded
                    try:
                        classCounter[classLab] += 1
                    except:
                        classCounter[classLab] = 1
                    #if True: # switch off desired_classes / classLimit constraints
                    if classLab in desired_classes: #and classCounter[classLab] <= classLimit:
                        print(Dir + "\\" + File)

                        # retrieve math data (formulae) from document
                        with open(datasetPath + "\\" + Dir + "\\" + File, "r", encoding="utf8") as f:
                            filestring = f.read()
                            formulae = BeautifulSoup(filestring, 'html.parser').find_all('formula')

                        # augment index
                        for formula in formulae:

                            formulaString = str(formula.contents)

                            # extract TeX formula
                            # formulaString
                            s = str(formula.contents)
                            start = 'alttext="'
                            end = '" display='
                            try:
                                #TeX = re.search('%s(.*)%s' % (start, end), s).group(1)
                                TeX = formula.contents[0].attrs['alttext']
                            except:
                                TeX = ""

                            # extract surrounding tex
                            index = filestring.find('alttext="' + TeX + '" display=')
                            surrounding_text_candidates = filestring[index - 500:index + 500]

                            for word in surrounding_text_candidates.split():
                                # lowercase and remove .,-()
                                word = word.lower()
                                char_excl = [".", ":", ",", "-", "(", ")",'=']
                                for c in char_excl:
                                    word = word.replace(c, "")
                                # not part of a formula environment
                                not_formula = not True in [ex in word for ex in excluded]
                                # not stopword
                                not_stopword = word not in stopwords
                                # not invalid html
                                #not_invalid = not True in [inv in word for inv in invalid]
                                # not a latin or greek letter
                                not_letter = word not in letters
                                if not_formula and not_stopword and not_letter: #and not_invalid
                                    #if TeX != "" and TeX not in stopwords and TeX not in letters:
                                    # check if around equation
                                    if '=' in TeX:
                                        try:
                                            formula_index[word][TeX] += 1
                                        except:
                                            try:
                                                formula_index[word][TeX] = 1
                                            except:
                                                formula_index[word] = {}
                                                formula_index[word][TeX] = 1

# save inverse semantic index formula catalog

with open(outputPath + 'inverse_semantic_index_formula_catalog.json','w',encoding='utf8') as f:
    json.dump(formula_index,f)

print("end")