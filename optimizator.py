import warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from numpy import array,sum,cumsum,argsort,where
from pandas import DataFrame
import random
from cost_function import *
from data_request import *
import config as c
from time import time


gamma = c.G
all_data = data_mine()
gen = array(all_data['generacion'])
precio = array(all_data['precio'])
consumo = array(all_data['consumo'])
B0 = all_data['SOC'][0]



def optimization(n = c.N):
    vec,est = [],[]
    
    
    for i in range(n):
        fun = F(B0,15,85)
        vec.append(fun[0])
        est.append(fun[1]) 

    obj = [G(v,gen,precio,consumo) for v in vec]    
    J = argsort(array(obj))
    cost = array(obj)[J[[0,1,2]]]
    vect = array(vec)[J[[0,1,2]]]
    est = array(est)[J[[0,1,2]]]
    risk = [R(v) for v in vect]
    df = DataFrame({
        'coste':cost.tolist(),
        'riesgo':risk,
        'operaciones':vect.tolist(),
        'estado':est.tolist()
    }) 
    
    nada = sum(precio*(consumo-gen))
    DF = df[(df.coste < nada)]
    best = DF.sort_values(by = "coste").iloc[0:3,:].sort_values(by = "riesgo")
    
    if len(best )== 0:
        best = df.sort_values(by = "coste").iloc[0:3,:].sort_values(by = "riesgo")
    
    
    
    no_software_ops = array([70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    no_software_ops[where(precio== max(precio))] = -70
    no_software_cost0 = sum(precio*(consumo - gen + gamma*no_software_ops))
    
    
    output = {
        'riesgo':float(best.iloc[0,1]),
        'coste':float(best.iloc[0,0]),
        'no_battery':float(nada),
        'no_software':float(no_software_cost0),
        'reduction': float(100*((no_software_cost0 - best.iloc[0,0])/no_software_cost0)),
        'operaciones': best.iloc[0,2],
        'estado': best.iloc[0,3],
        # 'pruebas': float(n)
    }
    return output

