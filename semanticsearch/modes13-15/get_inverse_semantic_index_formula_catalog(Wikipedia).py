from os import listdir
import json
from bs4 import BeautifulSoup

# Set file paths
basePath = 'D:\\NTCIR-12_MathIR_Wikipedia_Corpus\\'

datasetPath = basePath
outputPath = basePath + "output_RE\\"

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

# Create inverse_semantic_index_formula_catalog
formula_index = {}

# Fetch content and labels of documents
for File in listdir(datasetPath):
    if File.endswith(".html"):
        print(File)

        # retrieve math data (formulae) from document
        with open(datasetPath + "\\" + File, "r", encoding="utf8") as f:
            filestring = f.read()
            formulae = BeautifulSoup(filestring, 'html.parser').find_all('annotation')

        # augment index
        for formula in formulae:

            TeX = str(formula.contents[0]).strip()

            # extract surrounding tex
            index = filestring.find(TeX)
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

with open(outputPath + 'inverse_semantic_index_formula_catalog(Wikipedia).json','w',encoding='utf8') as f:
    json.dump(formula_index,f)

print("end")