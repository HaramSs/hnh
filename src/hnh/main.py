from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi import Request
import random
from transformers import pipeline
import io
from hnh.utils import get_max_label

app = FastAPI()

html = Jinja2Templates(directory="public")

@app.get("/hello")
def read_root():
    return {"Hello": "hotdog"}

@app.get("/")
async def home(request: Request):
    hotdog = "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQweb_7o7OrtlTP75oX2Q_keaoVYgAhMsYVp1sCafoNEdtSSaHps3n7NtNZwT_ufZGPyH7_9MFcao_r8QWr3Fdz17RitvZXLTU4dNsxr73m6V1scsH3_ZZHRw&usqp=CAE"
    dog = "https://hearingsense.com.au/wp-content/uploads/2022/01/8-Fun-Facts-About-Your-Dog-s-Ears-1024x512.webp"
    image_url = "data:image/png;base64,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"
    return html.TemplateResponse("index.html",{"request":request, "image_url": image_url})


@app.get("/predict")
def hotdog():
    model = pipeline("image-classification", model="julien-c/hotdog-not-hotdog") 
    return {"Hello": random.choice(["hotdog", "not hotdog"])}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    model = pipeline("image-classification", model="julien-c/hotdog-not-hotdog")
    
    from PIL import Image
    img = Image.open(io.BytesIO(img))  # 이미지 바이트를 PIL 이미지로 변환
    
    p = model(img)
    label = get_max_label(p)

    return {"label": label, "p": p} 

