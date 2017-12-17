import os, sys, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/ubuntu/Formual_Calculation')

from calculation import app as application
