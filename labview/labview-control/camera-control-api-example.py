from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "LabVIEW test"}

@app.get("/labview-get")
async def root():
    return 0