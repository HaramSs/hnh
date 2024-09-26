from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def root():
    #fastapi 
    return {"predict_result": "my_result"}
