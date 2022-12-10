#import ast
#import parser
#import re
from sympy.parsing.latex import parse_latex
from sympy.core.sympify import sympify
from sympy import Number, NumberSymbol, Symbol
#import scipy.constants
contant={'pi':'3.141592653589793','golden':'1.618033988749895','golden_ratio':'1.618033988749895','c':'299792458.0','speed_of_light':'299792458.0','mu_0':'1.2566370614359173e-06',\
         'epsilon_0':'8.854187817620389e-12','Planck':'6.62607004e-34','hbar':'1.0545718001391127e-34','G':'6.67408e-11','mu_{0}':'1.2566370614359173e-06',\
         'gravitational_constant':'6.67408e-11','g':'9.80665','e':'1.6021766208e-19','elementary_charge':'1.6021766208e-19','gas_constant':'8.3144598',\
         'alpha':'0.0072973525664','fine_structure':'0.0072973525664','N_A':'6.022140857e+23','Avogadro':'6.022140857e+23','k':'1.38064852e-23',\
         'Boltzmann':'1.38064852e-23','sigma':'5.670367e-08','Stefan_Boltzmann':'5.670367e-08','Wien':'0.0028977729','Rydberg':'10973731.568508',\
         'm_e':'9.10938356e-31','electron_mass':'9.10938356e-31','m_p':'1.672621898e-27','proton_mass':'1.672621898e-27','m_n':'1.672621898e-27','neutron_mass':'1.672621898e-27','S':'5.24411510858423962092'}

def prepformula(formula):
    """
        Process of formula
    """
    
    replace={"{\displaystyle":"","\\tfrac":"\\frac","\\left":"","\\right":"","\\mathrm":"","\\textbf":"","\\begin":"","\end":"","\\bigg":"","\\vec":""}    
    
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
    
def getlatexformula(formula):
    pformula=prepformula(formula)
    f=parse_latex(pformula)
    global latexformula
    latexformula=sympify(f)
    return latexformula 


def evalformula(formula):
    
    latexformula= getlatexformula(formula)
    l=sympify(latexformula)
    symbol=l.atoms(Symbol)
    return symbol   
    
    

def equality(formula,ext):
    global lhs
    global rhs    
    lhs,rhs=formula.split(ext,1)    
    value=evalformula(rhs)
    return value

    
    
def formuladivision(formula): 
       
    k = ['=', '\leq', '\req', '\\approx']         
    if '=' in formula:
        ext = '='              
        return ext
                    
    if '\leq' in formula:
        ext = '\leq' 
        return ext
                
    if '\req' in formula:
        ext = '\req'  
        return ext
                
    if '\\approx' in formula:
        ext = '\\approx'           
        return ext
                
    if not any(ext in formula for ext in k):   
        return None

class Formulacalculation:
    
    def __init__(self, request):
        self.formula = request
        print(self.formula)
    
    def answer(self):
        try:
            
            formula=self.formula
            global seprator 
            seprator= formuladivision(formula)            
            if seprator is not None:
                symbol=equality(formula,seprator)
            else:
                symbol=evalformula(formula)                               
            return symbol
            
        except Exception as e : print(e)
        
        
