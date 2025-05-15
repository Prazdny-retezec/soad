from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "LabVIEW test"}

@app.get("/should-capture-photo")
async def root():
    return 1

@app.get("/photo-path")
async def get_photo_path():
    return r"C:\Users\david\Mendelu\ASS_NSS\soad\labview\labview-control\output"