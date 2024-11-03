from fastapi import FastAPI
import uvicorn
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.get("/")
def read_root():
    return {"Hello": "World" + str(random.random())}

if __name__ =='__main__' :
    uvicorn.run(app,host='0.0.0.0',port=8000)