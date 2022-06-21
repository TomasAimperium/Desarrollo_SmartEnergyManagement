# Desarrollo de la aplicación de Smart Energy Management

Desarrollo de módulo de gestión de barterías para plantas solares fotovoltáicas. Este módulo emplea técnicas de optmización para gestionar el uso de baterías con el objetivo de reducir los costes (en el caso de industrias) o maximizar las ganancias (en el caso de generación). 

El proyecto consta de los siguientes archivos:


* config.py: parámetros necesarios para relizar la optimización. Este cuenta con los siguientes parámetros:

  * H: número de datos que se obtienen sobre el precio de la energía eléctrica.
  * G: eficiencia de la batería, mide la energía que es capaz de generar (consumir) una batería cuando esta se descarga (carga) al 100% 
  * N: número de iteraciones del algoritmo, cuánto mayor sea este número más tiempo tardará en realizar la optimización, pero mayor será el ahorro.
  * I: parámetro interno de la API de toma de datos.
  * today: fecha actual
  * tomor: fecha del día siguiente.
  
* data_request.py: script encargado de descargar de una API los precios de la potencia. Además, formatea los datos de forma adecuada para que estos puedan ser usados por el optimizador. Estos datos necesarios se muestran más abajo.

* cost_function.py: script que almacena las funciones de coste que se desean optimizar. Cuenta con 3 funciones:
  
  * F: calcula el coste (beneficio) por hora, así como las intervenciones en la batería que generan esos valores de coste.
  * G: evalua  el coste (beneficio) total diario.
  * R: calcula el riesgo que supone para la barería esas operaciones.


* optimizator.py: es el script encargado cargar los datos preprocesados de precios, generación y posible consumo. Una vez cargados se realizan operaciones de optimización del coste mediante iteraciones de la función de coste presente en cost_function.py. 

* SOH_monitoring.py: este script, con los datos de la batería se calculan los valores de estado de salud de la batería. El objetivo último es predecir el estado de salud de la batería cuando se tengan muchos valores.

* main.py: este script habilita una API local que permite realizar POST que devuelven los datos calculados por optimizator.py y SOH_monitoring.py.


## Estructura de datos de salida

A continuación se da la estructura de valores de salida del modulo:

all_data = {
    'generacion':[0.0, 0.0, 0.0, 0.,0.59726962, 0.0,  1.96245734, ...
    'precio':[0.23097,0.22283,0.22402,0.22674,0.22606,0.23865, ...
    'consumo':[9.49694405,   7.94546309,   8.09993955, 7.71039022, ...
    'SOC': [75]
}

## Datos de entrada necesarios

Los datos que se necesitan proporcionar para que sea posible llevar a cabo la optimización  de la batería son los siguientes.


* Datos sobre el precio de la energía en el pais a analizar. Estos pueden venir de API o de algún tipo de base de datos, sobre las que trabajar.

* Datos de generación: se necesitan datos de generación de las placas solares. Estos pueden obtenerse de varias formas:
  
  * Mediante modelización con los valores de irradiancia obtenidos por API y obtenidos mediante procesos de predicción
  * En caso de que no se tenga los valores de irradiancia, estos pueden estimarse con valores meteorológicos de API, como puede ser temperatura, humedad, etc.
  * Por último, estos datos también pueden ser predichos usabdo predicción de series de tiempo mediante valores históricos.

* Datos de consumo: serie de tiempo de datos de consumo (en caso de que sea una industria), es decir, el coste energético en cada franja de tiempo en el día que se quiera optimizar. En el caso de que no se tengan estos datos, será necesario conocer el histórico de datos para poder así predecirlos, a pesar de que esto supodrá un descenso de la calidad de la optimización, ya que no se conocerá con exactitud los valores que se obtendrán de coste o beneficio de cada operación.

* Datos de batería: con el objetivo de parametrizar el comportamiento de la batería es necesario conocer variables de la misma, el objetivo es conocer tanto el estado de carga (SOC) antes de realizar la optimización y el estado de salud (SOH). Las variables deseadas son:
 
  * SOC o en su defecto valores de carga eléctrica: esto es necesario para iniciar la simulación ya que sin estado de carga inicial, no se puede conocer la disponibilidad de la batería al inicio del día. Por lo tanto, este valor es de vital importancia para la optimización.
  * corriente: los valores de corriente eléctrica son de vital importancia para conocer el estimar el estado de salud de la batería.
  * voltaje o diferencia de potencial y temperature: estos valores no son obligatorios, a no se que no se dispongan de datos de SOC o carga eléctrica de la batería, ya que este valor es estimable mediante modelos de ML, pero suponen un empeoramiento de los resultados respecto a las lecturas directas en la batería.


Hay que tener en cuenta que para que el la función de optimización funcione correctamente, los datos tienen que tener la misma granularidad (o menor) que el valor de la granularidad de los precios, es decir, si el precio se da cada hora, como mínimo los datos de consumo deben proporcionarse cada hora. En caso de que esto no sea posible, los datos deberán ser interpolados, lo cual hará que se pierda precisión en la optimización.


## Estructura de datos de salida

Para la optimización:

       {       
        "riesgo":1.1007499893768526,
        "coste":-331.6737653122391,
        "no_battery":32505.19823468775,
        "no_software":26925.918234687728,
        "reduction": 101.23180113087085,
        "operaciones": [37,-35,25,19,...
        "estado": [30,67,32,57,76,66,...
        }

Para el estado de salud:

      {
      "SOH_today": [99.34, 99.12 ,99.99 ,99.67 ,99.12],
      "SOH_his": [99.11, 99.07, 98.44, 98.92, 98.10,...
      }
    
