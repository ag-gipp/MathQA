## Math-aware QA system

This system is able to answer mathematical questions (general, geometry, relationships) asked in natural language by the user. Moreover, identifier symbol name and value display as well as calculation functionality is provided. Labeled formula data is retrieved from Wikidata: https://wikidata.org

You find a deployed version hosted by Wikimedia at https://mathqa.wmflabs.org

## System setup
```
sudo apt-get install python3
virtualenv -p python3 venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
./dependencies-ppp.sh
python app.py
```

## CoreNLP

CoreNLP is resposible for the extraction of triples (subject, predicate, object) from the questions.

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

## Pywikibot
Pywikibot is used to extract the formula concept data from Wikidata:
https://tools.wmflabs.org/pywikibot

## latex2sympy-master
Used to convert variants of LaTeX formula strings to Sympy equivalent form.

ANTLR is used to generate the parser:
```
sudo apt-get install antlr4
```

Download latex2sympy from https://github.com/augustt198/latex2sympy

## Sympy
```
apt-get install python3-sympy
```

## ppp_modules
```
pip3 install --user ppp_questionparsing_grammatical
pip3 install git+https://github.com/ProjetPP/PPP-datamodel-Python.git
pip3 install git+https://github.com/ProjetPP/PPP-libmodule-Python.git
```

## xmltodic
```
pip3 install xmltodict
```
## Flask
```
pip3 install Flask
```
## After installing all the libraries follow these steps to run the Math-aware QA system:
1) run the CoreNLP Server
```
Mathaware-Q-A-System/CoreNLP$ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 &
SERVER_PID=$!
```
2) run the Flask server
```
Mathaware-Q-A-System$ export FLASK_APP=app.py
Mathaware-Q-A-System$ flask run
```
Then you can start the system in your browser by opening the localhost: http://localhost:5000
