import warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from datetime import date,timedelta

H = 24 #numero de datos
G = 100 #eficiencia de la bateria
N = 10000#int(1e4) #numero de pruebas
I = "1" #lugar
# E = 0.8 #eficiencia de la planta
today = date.today().strftime("%d-%m-%Y")
tomor = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")
