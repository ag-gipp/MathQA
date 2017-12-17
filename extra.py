import ast
import parser
import re 
from process_latex import process_sympy
from sympy.core.sympify import sympify
from sympy import Number, NumberSymbol, Symbol
import sympy
#import scipy.constants
import json
'''
text = open('/home/kaushal/gold.json').read()
d = json.loads(text)
for each in d:
                #c+=1
                #print(c)
    formula=each["math_inputtex"]
    print(formula)
'''


contant={'pi':'3.141592653589793','golden':'1.618033988749895','golden_ratio':'1.618033988749895','c':'299792458.0','speed_of_light':'299792458.0','mu_0':'1.2566370614359173e-06',\
         'epsilon_0':'8.854187817620389e-12','Planck':'6.62607004e-34','hbar':'1.0545718001391127e-34','G':'6.67408e-11',\
         'gravitational_constant':'6.67408e-11','g':'9.80665','e':'1.6021766208e-19','elementary_charge':'1.6021766208e-19','gas_constant':'8.3144598',\
         'alpha':'0.0072973525664','fine_structure':'0.0072973525664','N_A':'6.022140857e+23','Avogadro':'6.022140857e+23','k':'1.38064852e-23',\
         'Boltzmann':'1.38064852e-23','sigma':'5.670367e-08','Stefan_Boltzmann':'5.670367e-08','Wien':'0.0028977729','Rydberg':'10973731.568508',\
         'm_e':'9.10938356e-31','electron_mass':'9.10938356e-31','m_p':'1.672621898e-27','proton_mass':'1.672621898e-27','m_n':'1.672621898e-27','neutron_mass':'1.672621898e-27','S':'5.24411510858423962092'}
def prepformula(formula):
    
    replace={"{\displaystyle":"","\\tfrac":"\\frac","\\left":"","\\right":"","\\mathrm":"","\\textbf":"","\\begin":"","\end":"","\\bigg":"","\\vec":"","\cdots":""}    
    
    if formula.startswith('{\displaystyle') and formula.endswith('}'):
        fformula=formula.rsplit('}',1) 
        return replace_all(fformula[0],replace)       
        
    if formula.endswith('.'):        
        fformula=formula.split('.')
        return replace_all(fformula[0],replace) 
        
    if formula.endswith(","):        
        fformula=formula.split(',')
        return replace_all(fformula[0],replace) 
        
    else:   
        return replace_all(formula,replace) 
        
    
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text    
    
    


def evalformula(formula):
    try:
        f=process_sympy(formula)
        a=sympify(f)
        symbol=a.atoms(Symbol)
        return (list(symbol))
    except:
        return "error"
        pass
    
    '''
    identifier={}
    
    for x in symbol:
        if str(x) in contant:
            value=contant.get(str(x))            
            identifier[x]=value
        else:
            data = float(input("Enter a value for" +  " " + str(x) +":"))
            identifier[x]=data
                    
    value=a.evalf(subs=identifier)
    print(value)
    return value 
    '''
    
    

def equality(formula,ext):    
    lhs,rhs=formula.split(ext,1)    
    value=evalformula(rhs)
    return value
    #value1=evalformula(lhs)
    #print(value)
    #print(value1)
    
            
    #if value1 is not None:
     #   return ("value of %s : = %.2e" % (rhs,value1))
                
    #if value is not None:    
     #   return ("value of %s : = %.2e" % (lhs,value))   
     
def value(formula):
    try:
        f=process_sympy(formula)
        a=sympify(f)
        symbol=a.atoms(Symbol)
        identifier={}
        return (list(symbol))
    except:
        return "error"
        pass
    
    '''
    identifiers={}
    
    for x in symbol:
        if str(x) in contant:
            value=contant.get(str(x))            
            identifier[x]=value
        
        else:
            data = float(input("Enter a value for" +  " " + str(x) +":"))
            identifier[x]=data
    print(identifier)  
    #identifiers1={'aleph_0': '6.0', 'omega': '5.0', 'alpha: '0.0072973525664'}
    value=a.evalf(subs=identifiers) 
    
    print(value)
    return ("value of equation := %.2e" % value)
    '''



dict={}
#formula="W(2, k) > 2^k/k^\\varepsilon"
def answer():
        try:
                text = open('/home/kaushal/gold.json').read()
                d = json.loads(text)
            #for each in d:                
                #formula=each["math_inputtex"]
                formula="\\bar{V}^*"
                preprocessedformula=prepformula(formula)
                #print(preprocessedformula)
                k=['=','\leq','\req','\\approx','\le']
            
                if '=' in preprocessedformula:
                    ext='='           
                    val=(equality(preprocessedformula,ext))
                    dict[preprocessedformula]=val
                if '\leq' in preprocessedformula:
                    ext='\leq'           
                    val=equality(preprocessedformula,ext)
                    dict[preprocessedformula]=val
                if '\req' in preprocessedformula:
                    ext='\req'           
                    val= equality(preprocessedformula,ext)
                    dict[preprocessedformula]=val
                if '\le' in preprocessedformula:
                    ext='\le'           
                    val=equality(preprocessedformula,ext)
                    dict[preprocessedformula]=val
                if '\\approx' in preprocessedformula:
                    ext='\\approx'           
                    val= equality(preprocessedformula,ext)
                    dict[preprocessedformula]=val
                    
                if not any(ext in preprocessedformula for ext in k):   
                    val=(value(preprocessedformula)) 
                    dict[preprocessedformula]=val
                for k,v in dict.items():
                    print (k,v)
            #import json
            #with open('/home/kaushal/Desktop/test.json', 'w') as fp:
            #json_string = json.dumps(dict)
            #print(json_string)    
        except Exception as e : print(e)
        
        
answer()    

   
