import warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


from numpy import array,min,std,sum
from random import randint
import config as c


hours = c.H
gamma = c.G
n = c.N

def F(B,Bmin,Bmax):
    bateria,estado = [],[]
    for i in range(hours):
        estado.append(B)
        B0 = randint(Bmin-B, Bmax - B)
        B += B0
        bateria.append(B0)
    return [bateria,estado]

def G(bateria,gen,precio,consumo):
    C = sum(precio*(consumo - gen + gamma*array(bateria)))
    return C


def R(bateria):
    dano = array(bateria)[array(bateria) > 0]
    dano_ = abs(array(bateria)[array(bateria) < 0])
    R = (len(dano)*min(dano)/std(dano) + len(dano_)*min(dano_)/std(dano_))/2
    return R