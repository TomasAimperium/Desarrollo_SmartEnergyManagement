from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from optimizator import *
from SOH_monitoring import *
import uvicorn
from numpy import where

app = FastAPI()

class StockIn(BaseModel):
    inputs: dict
    
    

@app.get("/")
async def root():
    return {"message":"Todo correcto con la api"}



@app.post("/predict")
def get_prediction(payload: StockIn):
    
    
    c,d = [],[]

    for i in range(1000):
        print(i)
        out = optimization()
        d.append(out)
        c.append(out['coste'])
        
    D = d[np.where(c == min(c))[0][0]]
    
    
    
    
    dall = {}
    
    dall.update(dict(D))
    dall.update(SOH_state())
    
    
    
    return dall
    


# @app.post("/train")#, response_model=StockOut, status_code=200)
# def get_ptrain():
#     return train()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn app.main:app --reload