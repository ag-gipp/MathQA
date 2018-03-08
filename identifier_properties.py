from flask import Flask, render_template

import pywikibot
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
import xmltodict
import json, sys

app = Flask(__name__)

# @app.route('/')
# def my_form():
#     return render_template("index.html")

# formula Wikidata QID identifier search strings
formula = "Q11432"
identifier = "R"

@app.route('/')
def enter_formula():
    return render_template("index.html")

@app.route('/identifier_properties')
def retrieve_identifier_properties():

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""#find identifier name
        SELECT ?identifierLabel ?symbol WHERE {
        wd:""" + formula + """ p:P527 ?statement. #p: points to statement node
        ?statement ps:P527 ?identifier. #ps: property statement
        ?statement pq:P2534 ?symbol. #ps: property qualifier
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }""")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        tmp_results = []
        for result in results["results"]["bindings"]:
            tmp_results.append(result)

        json_str = json.dumps(tmp_results)
        resp = json.loads(json_str)
        #return resp['identifierLabel']['value']
        return json_str

    except:
        return "NA"

@app.route('/identifier_name')
def retrieve_identifier_name():

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""#find identifier name
        SELECT ?identifierLabel WHERE {
        wd:""" + formula + """ p:P527 ?statement. #p: points to statement node
        ?statement ps:P527 ?identifier. #ps: property statement
        ?statement pq:P2534 ?symbol. #ps: property qualifier
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        FILTER(CONTAINS(STR(?symbol), '<mi>""" + identifier + """</mi>'))
        }""")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        tmp_results = []
        for result in results["results"]["bindings"]:
            tmp_results.append(result)

        json_str = json.dumps(tmp_results[0])
        resp = json.loads(json_str)
        return resp['identifierLabel']['value']
        # return json_str

    except:
        return "NA"

@app.route('/identifier_value')
def retrieve_identifier_value():

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""#find identifier value
        SELECT ?value WHERE {
        wd:""" + formula + """ wdt:P527 ?identifier.
        ?identifier wdt:P416 ?symbol.
        ?identifier wdt:P1181 ?value.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        FILTER(STR(?symbol) = '""" + identifier + """')
        }""")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        tmp_results = []
        for result in results["results"]["bindings"]:
            tmp_results.append(result)

        json_str = json.dumps(tmp_results[0])
        resp = json.loads(json_str)
        return resp['value']['value']

    except:
        return "NA"

if __name__ == '__main__':
    app.run(debug=True)