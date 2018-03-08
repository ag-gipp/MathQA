##Matheaware QA system

This system is able to answer mathematical questions asked in natural language by the user.


##System setup

sudo apt-get install python3

##CoreNlp

CoreNlp is resposible for extraction Triple (subject, predicate, object) from the questions.

1)  Downloading POS Tagger


wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-12-09.zip

2)  Installing POS Tagger


unzip stanford-postagger-full-2015-12-09.zip

3)  Cloning and installing CoreNLP


    git clone https://github.com/stanfordnlp/CoreNLP.git
    cd CoreNLP
    ant compile
    ant jar
    cd ..
4) Downloading English model for CoreNLP


wget http://nlp.stanford.edu/software/stanford-english-corenlp-2016-01-10-models.jar

##Pywikiwot
Pywikibot is used to extract the formula from Wikidata
https://tools.wmflabs.org/pywikibot/

##latex2sympy-master
Used to convert variant of latex formula to sympy equivalent form


ANTLR is used to generate the parser:

    sudo apt-get install antlr4
For latex2sympy download from

https://github.com/augustt198/latex2sympy

##sympy
apt-get install python3-sympy

##ppp_modules

pip3 install --user ppp_questionparsing_grammatical

pip3 install git+https://github.com/ProjetPP/PPP-datamodel-Python.git

pip3 install git+https://github.com/ProjetPP/PPP-libmodule-Python.git

##xmltodic
pip3 install xmltodict

##flask
pip3 install Flask

## After installing all the libraries follow the steps to run the Matheaware QA system:
1) run the CoreNLP Server
```
kaushal@kaushal:/workspace1/matheaware_Q-A_system/CoreNLP# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 &
SERVER_PID=$!
```
2) run the flask server
```
kaushal@kaushal:/workspace1/matheaware_Q-A_system/$ export FLASK_APP=calculation.py
kaushal@kaushal:/workspace1/matheaware_Q-A_system/$ flask run
```
Then you can see the the system in your browser by opening the localhost which is : http://127.0.0.1:5000/
