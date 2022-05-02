from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse

import os
from os import getcwd
from PIL import Image
from typing import List
import datetime

app = FastAPI()

PATH_FILES = getcwd() + "/"


def resize_image(filename: str):
    sizes = [{
        "width": 256,
        "height": 256
    }]

    for size in sizes:
        size_defined = size['width'], size['height']
        currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        saved_file_name = ''.join([currentTime,'_',filename])

        image = Image.open(PATH_FILES + filename, mode="r")
        image.thumbnail(size_defined)
        image.save(PATH_FILES + "static/" + "images/" + str(size['width']) + "X" + str(size['height']) + "_" + saved_file_name)
    print("success")


@app.post("/upload/file2")
async def upload_file(background_tasks: BackgroundTasks, in_files: List[UploadFile] = File(...)):
    file_urls = []
    for file in in_files:
        
        # SAVE FILE ORIGINAL
        with open(PATH_FILES + file.filename, "wb") as myfile:
            content = await file.read()
            myfile.write(content)
            myfile.close()

        # RESIZE IMAGES
        background_tasks.add_task(resize_image, filename=file.filename)
        file_urls.append(PATH_FILES + file.filename)
    # return FileResponse(file_urls[0])
    return JSONResponse(content={"message": file_urls})