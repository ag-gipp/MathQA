# -*- coding: utf-8 -*-
"""Request handler of the module."""

import pywikibot
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
import xmltodict

formula = defaultdict(list)

def get_formula(sub, lang="en"):
    """
        Get subject number and language 
        Return value of defining formula property:P2534
    """
    try:
        subject = str(sub)
        site = pywikibot.Site(lang, "wikipedia")
        page = pywikibot.Page(site, subject)
        item = pywikibot.ItemPage.fromPage(page)
        subn = str(item).replace("[[wikidata:", '').replace("]]", '')
        # Get the claim dictionary
        item_dict = item.get()
        clm_dict = item_dict["claims"]

        # Get the defining formula property:P2534
        for clm in clm_dict["P2534"]:
            key = clm.getTarget()
            # todo: call identfier_properties
            return key

    except:
        s = "System could not find the formula for %s . If you know the formula \
        you can set the defining formula property <a href='https://www.wikidata.org/wiki/P2534' target='_blank'>P2534</a> in %s \
        <a href='https://www.wikidata.org/wiki/%s' target='_blank'>%s</a>" % (sub, sub, subn, sub)
        return s

    ''' 
    try:   
        for clm in clm_dict["P527"]:
            #c=clm.getTarget()
            json=clm.toJSON()
            #print(json)
            #print(json['qualifiers']['P2534'][0]['datavalue']['value'])
            formula[key].append(json['qualifiers']['P2534'][0]['datavalue']['value'])
            return formula
        
    except:
        return key    
    '''


def get_formula_geometry(sub, pred, subject, predicate):
    """
        Get subject and predicate number
        Return value of has quality property : P1552
    """
    subn = str(sub).replace("[[wikidata:", '').replace("]]", '')
    predn = str(pred).replace("[[wikidata:", '').replace("]]", '')

    item_dict = sub.get()
    clm_dict = item_dict["claims"]
    try:
        # get the has quality property:P1552
        for clm in clm_dict["P1552"]:
            c = clm.getTarget()
            if c == pred:
                c = clm.toJSON()
                return (c['qualifiers']['P2534'][0]['datavalue']['value'])

        else:
            s = "System could not find the formula for %s . If you know the formula \
                you can set the has quality property  <a href='https://www.wikidata.org/wiki/P1552' target='_blank'> P1552 </a> \
                in <a href='https://www.wikidata.org/wiki/%s' target='_blank'> %s </a> for <a href='https://www.wikidata.org/wiki/%s' target='_blank'> %s </a>" % (
            subject, subn, subject, predn, predicate)
        return s


    except:
        s = "System could not find the formula for <a href='https://www.wikidata.org/wiki/%s' target='_blank'> %s </a> " % (
        subn, subject)
        return s


def get_formula_sparql(sub, pred):
    """
        Get subject and predicate number 
        return formula
    """
    # subn=str(sub).replace("[[wikidata:",'').replace("]]",'')
    # predn=str(pred).replace("[[wikidata:",'').replace("]]",'')

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    try:
        q = """
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        
        SELECT ?qid ?qformula WHERE {
            ?qid wdt:P527 wd:%s.
              ?qid wdt:P527 wd:%s.
              ?qid wdt:P2534 ?qformula.
              
          
          }""" % (sub, pred)
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            # print(result["p"]["value"]) + " " + result["w"]["value"]
            a = result["qformula"]["value"]

        result = xmltodict.parse(a)
        return (result['math']['semantics']['annotation']['#text'])

    except:
        s = "System could not find the formula for <a> %s </a> and <a> %s </a>" % (sub, pred)
        return s


Hindigeolist = ['क्षेत्रफल', 'आयतन', 'समुद्र तट से ऊंचाई', 'लम्बाई', 'विकर्ण', 'सतह क्षेत्र', 'लंबाई']


def get_item_number(subject, predicate, lang="en"):
    """
        Get subject, predicate and language
        Return formula
    """

    try:
        usub = str(subject)
        upred = str(predicate)
        site = pywikibot.Site(lang, "wikipedia")
        subjecti = pywikibot.Page(site, usub)
        sitem = pywikibot.ItemPage.fromPage(subjecti)
        predicatei = pywikibot.Page(site, upred)
        pitem = pywikibot.ItemPage.fromPage(predicatei)
        subn = str(sitem).replace("[[wikidata:", '').replace("]]", '')
        predn = str(pitem).replace("[[wikidata:", '').replace("]]", '')
        if (lang == "en"):
            return get_formula_geometry(sitem, pitem, usub, upred)
        if upred in Hindigeolist:
            return get_formula_geometry(sitem, pitem, usub, upred)
        else:
            return get_formula_sparql(subn, predn)
    except:
        s = "System could not find the item <a> %s </a>" % (usub)
        return s


geometry = ['surface area', 'volume', 'area', 'radius of circle', 'altitude', 'diagonal', 'medians', 'inradius',
            'circumradius', 'length']
formulalist = ['formula', 'equation', 'mathematical formula']


def predicate(predicate, subject):
    if predicate in geometry:
        return get_item_number(subject, predicate)
    elif predicate in formulalist:
        return get_formula(subject)
    else:
        s = "System could not find the item <a> %s </a> for <a> %s </a>" % (predicate, subject)
        return s


class FormulaRequestHandler:

    def __init__(self, request):
        self.request = request

    def answer(self):
        #request = self.request
        request = self.request[0]._attributes['tree']._attributes
        #formula = predicate(request.predicate.value, request.subject.value)
        formula = predicate(request['predicate'].value, request['subject'].value)
        return formula


class HindiRequestHandler:

    def __init__(self, language, subject, predicate):
        self.language = language
        self.subject = subject
        self.predicate = predicate

    def answer(self):

        Hindiformulalist = ['गणितीय सूत्र', 'सूत्र', 'फार्मूला']
        if self.predicate in Hindiformulalist:
            return get_formula(self.subject, self.language)
        else:
            return get_item_number(self.subject, self.predicate, self.language)
