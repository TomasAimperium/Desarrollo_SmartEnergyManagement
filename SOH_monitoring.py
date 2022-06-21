import pandas as pd
import json
import numpy as np


def SOH_state():
    f = open ('inp_battery.json', "r")

    inp = json.loads(f.read())

    C0 = inp['C0']

    DF = pd.DataFrame(inp['battery_data']).reset_index(drop = True)
    DF['Gradient'] = np.gradient(DF.SOC)
    DF = DF[DF['Gradient']>0].reset_index(drop = True)

    ASOC = []
    Q = []
    for cy in np.unique(DF.cycle):
        c = DF[DF.cycle == cy]
        ASOC.append(c.SOC.values[-1] - c.SOC.values[0])
        Q.append(np.trapz(c.current,dx = 2.133333))  

    ASOC = np.array(ASOC)
    Q = np.array(Q)


    C = Q[np.where(Q > 30)]/ASOC[np.where(ASOC > 30)]
    C0 = max(C)
    SOH_today = 100*C/C0

    out = {
        "SOH_today":list(SOH_today),
        "SOH_his":list(100*np.array(inp['SOH_hist']))
    }
    
    return out