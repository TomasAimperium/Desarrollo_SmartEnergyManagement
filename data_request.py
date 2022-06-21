import warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import config as c
from requests import get
from json import loads,load
from numpy import array
from pandas import DataFrame
from tensorflow.keras.models import load_model


def find_prize(uri):
    '''
    funcion que hace cosas
    '''
    httpheader = {'Authorization': 'Token token="fa43fac0b5171af148b563cebaef0b1099ac5ebaf1dae2391ce3997b99ea409c"'}
    extraccion = get(uri, headers = httpheader)
    data = loads(extraccion.text)
    D = data['indicator']['values']
    value = []
    datetime = []
    geo_name = []
    for d in D:
        value.append(float(d['value']))
        datetime.append(int(d['datetime'][11:13]))
        geo_name.append(d['geo_name'])


    df = DataFrame({
        'precio': value,
        'hora': datetime,
        'region':geo_name
    })
    iden = c.I
    geo_id = {
        "1": "Península",
        "2": "Canarias",
        "3": "Ceuta",
        "4": "Melilla"
    }
    precios = df[df.region == geo_id[iden]]
    return precios.precio.values/1000



def data_mine():
    #se cargan los datos
    f = open('inp.json')
    data = load(f)


    #datos de consumo
    consumo = data['consumo']


    if len(data['irradiancia']) == 0:
        #se obtiene irradiancia
        model_irr=load_model('modelos/meteorologia.h5')
        irradiancia = model_irr.predict(array(data['meteodata']))
    else:
        irradiancia = data['irradiancia']

    #se obtiene la generacion
    model_gen=load_model('modelos/generacion.h5')
    generacion = model_gen.predict(irradiancia) 



    #se obtiene el precio
    uri = "https://api.esios.ree.es/indicators/1001?vis=2"
    uri += "&start_date=" + str(c.today) + "T00:00:00+02:00"
    uri += "&end_date=" + str(c.tomor) + "T01:00:00+02:00"
    uri += "&geo_agg=sum&geo_ids&time_trunc=hour&time_agg=&locale=es&geoids=8741"
    precio = find_prize(uri)


    #estado de carga de la bateria SOC
    electric =  array(data['battery'])
    model_soc= load_model('modelos/SOC.h5')
    SOC = model_soc.predict(electric)

    #unimos todos los datos
    all_data = {
        'generacion':generacion,
        'precio':precio,
        'consumo':consumo,
        'SOC': [int(100*SOC[0][0])]
    }
    return all_data





# gen = [ 0.        ,  0.        ,  0.        ,  0.        ,  0.59726962,
#         0.        ,  1.96245734, 10.43393467, 25.95752749, 50.90199902,
#        64.28571429, 85.727583  , 96.47326507, 81.99002363, 75.76791809,
#        60.25442135, 38.68031854, 16.29692833,  4.3003413 ,  1.53583618,
#         0.        ,  0.        ,  0.        ,  0.        ]


# consumo = [  9.49694405,   7.94546309,   8.09993955, 7.71039022,
#          7.57606287,   8.65068171,   9.49694405,  65.08438306,
#        130.09873061, 126.12834979, 121.21080612, 135.34555712,
#        154.67795016, 142.29852634, 110.39693734, 105.87682181,
#         78.04654443,  11.56558533,  10.36671368,  12.03573108,
#          9.81664316,   9.16784203,   9.23836389,  12.81930732]



# precio = [0.23097,0.22283,0.22402,0.22674,0.22606,0.23865,
#           0.28527,0.30198,0.32166,0.30266,0.32726,0.29976,
#           0.29317,0.28031,0.22635,0.22973,0.23122,0.23177,
#           0.28044,0.31917,0.35194,0.36727,0.31477,0.30727]





