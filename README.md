# Math-aware QA system

This system is able to answer mathematical questions (general, geometry, relationships) asked in natural language by the user. Moreover, identifier symbol name and value display as well as calculation functionality is provided. Labeled formula data is retrieved from Wikidata (https://wikidata.org), Wikipedia (https://wikipedia.org), and the arXiv preprint repository (https://arxiv.org) via SPARQL queries and dataset dumps.

## System setup
If you do not want to setup the system locally at your computer, you find a deployed version hosted by Wikimedia at https://mathqa.wmflabs.org
```
sudo apt-get install python3
virtualenv -p python3 venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
./dependencies-ppp.sh
python app.py
```

### CoreNLP
CoreNLP is responsible for the extraction of triples (subject, predicate, object) from the questions.

1)  Downloading POS Tagger
```
wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-12-09.zip
```

2)  Installing POS Tagger
```
unzip stanford-postagger-full-2015-12-09.zip
```

3)  Cloning and installing CoreNLP
```
git clone https://github.com/stanfordnlp/CoreNLP.git
cd CoreNLP
ant compile
ant jar
cd ..
```

4) Downloading the English model for CoreNLP
```
wget http://nlp.stanford.edu/software/stanford-english-corenlp-2016-01-10-models.jar
```

### Pywikibot
Pywikibot is used to extract the formula concept data from Wikidata:
https://tools.wmflabs.org/pywikibot
```
pip install pywikibot
```

### Sympy
The computer Algebra System (CAS) Sympy is used for the calculation module to get result values given a retrieved formula and user inputs for the variables.
```
apt-get install python3-sympy
```

### Latex2Sympy
Used to convert variants of LaTeX formula strings to Sympy equivalent form.

1) ANTLR is used to generate the parser:
```
sudo apt-get install antlr4
```

2) Download latex2sympy from https://github.com/augustt198/latex2sympy

### ProjetPP
The Projet Pensées Profondes (PPP) provides a Question Answering framework and some modules: https://projetpp.github.io
```
pip3 install --user ppp_questionparsing_grammatical
pip3 install git+https://github.com/ProjetPP/PPP-datamodel-Python.git
pip3 install git+https://github.com/ProjetPP/PPP-libmodule-Python.git
```

### Flask
Flask is the web framework middleware used as an interface between the frontend and the backend.
```
pip3 install Flask
```

## Run the system
1) Run the CoreNLP Server
```
Mathaware-Q-A-System/CoreNLP$ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 &
SERVER_PID=$!
```
2) Run the Flask server
```
Mathaware-Q-A-System$ export FLASK_APP=app.py
Mathaware-Q-A-System$ flask run
```
Then you can start the system in your browser by opening the localhost: http://localhost:5000

## Evaluation of system's performance
In the following we describe how to reproduce the evaluation results presented in the associated paper.

### Result tables
The result tables can be found in the 'evaluation' folder.

1) The 'evaluation/general' folder contains the MathQA performance and Wikidata seeding scores for general and geometry questions and their comparison to Wolfram Alpha.
2) The 'evaluation/semanticsearch' folder contains the results of the 15 different evaluation modes and for mode 15 a performance comparison of MathQA to Google and Wolfram Alpha.

<mark>Note that the commercial competitors are unable to provide results for modes 1-14 (hence for only 0.7% of the modes they are able) and MathQA has the additional advantage of being transparent (open source and open data).</mark>

### Evaluation scripts

1) The general evaluation was performed manually by a domain expert using the system's interfaces to get answers to sample questions (integrated system evaluation) and assessing their relevance.
2) The respective evaluation scripts to automatically generate result tables for expert assessment and scoring can be found in the folder 'semanticsearch'.

#### Sample dataset

1) The sample is chosen for the formula benchmark MathMLben: https://mathmlben.wmflabs.org
2) The formula annotation data (containing Wikidata Entity Linking markup) can be downloaded from
```
https://mathmlben.wmflabs.org/rawdata/all   
```
which is stored in the folder 'semanticsearch/mathmlben'.
3) The sample formula data can be found in 'semanticsearch/examples_list/formula_examples.json'. For each formula, the fields "GoldID", "formula_name", "formula_tex", "semantic_tex", "identifier_symbols", "identifier_names", and "identifier_qids" are populated. 
4) The script
```
evaluation_examples_seeding_list.py
```
can be used to retrieve the Wikidata item names from the QIDs for the respective formula identifiers.
5) By running
```
generate_evaluation_list_template.py
```
the identifier symbol-name template for the further is generated for further use in the evaluation modes 1-12.
6) The NTCIR-11/12 arXiv and Wikipedia used to generate the formula and identifier semantic formula index catalogs can be obtained from: http://ntcir-math.nii.ac.jp/data

#### Evaluation Modes

##### Modes 1-6

1) The identifier lists, statistics, index candidates, and semantics catalogs (generated from the NTCIR-11/12 arXiv and Wikipedia dataset) can be found in the 'arXiv...json' or 'Wikipedia...json' respectively.
2) By running
```
evaluate_{arXiv,Wikipedia,Wikidata}-Identifier_List.py
```
you get the evaluation tables for the different index sources.
3) The semantic catalogs can be analyzed using
```
identifier_index_statistics.py
```
4) The evaluation metric scores (Discounted Cumulative Gain and Top 1 accuracy) are calculated using
```
score_arXivWikipedia-Identifier_List.py
```

##### Modes 7-12
1) You find the formula and identifier (semantics) catalogs in the respective .pkl files.
2) The evaluation tables are generated using
```
SemanticSearch_{arXivWikipedia,Wikidata}_evaluation.py 
```
and scored using
```
SemanticSearch_{arXivWikipedia,Wikidata}_scores.py
```

##### Modes 13-15
1) The semantic formula catalog indices are generated using
```
get_inverse_semantic_index_formula_catalog({arXiv,Wikipedia})
```
2) The respective formula index can be analyzed running
```
formula_index_statistics.py
```
2) The (Score,Rank) tuples for the result tables are generated using
```
evaluate_inverse_formula_index.py
```
3) Finally, the Discounted Cumulative Gain (DCG) scores can be calculated using
```
score_inverse_formula_index.py
```