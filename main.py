from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Path
from pydantic import BaseModel
import uvicorn
from models import File
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import os
# from fastapi.responses import FileResponse
from datetime import datetime,date



app = FastAPI()

path = "C:/Users/Dell/Documents/fastapi/Files"

models.Base.metadata.create_all(bind= engine)

def get_db():
    try: 
       db = SessionLocal()
       yield db

    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]

class FileRequest(BaseModel):
    date_ :date = datetime.now()
    file_name : str 
    location : str

@app.get("/read_file")
async def read_file(db:db_dependency):
    now = datetime.now()
    filename = "MP3-1.mp3"
    location = os.path.abspath(filename)
    existing_file = db.query(File).filter(File.file_name == filename).first()
    if existing_file:
        existing_file.location = location
        existing_file.date = now
        db.commit()
        db_data = db.query(File).all()
        return existing_file, db_data
    else:
        file_data =  File(file_name = filename,location = location, date = now)
        db.add(file_data)
        db.commit()
        db_data = db.query(File).all()
        print(db_data)
        return file_data, db_data

    
    
@app.get("/read_files")
async def read_file(db:db_dependency):
    now = datetime.now()
    filename = "MP3-2.mp3"
    location = os.path.abspath(filename)

    file_data =  File(file_name = filename, location = location, date = now)
    db.add(file_data)
    db.commit()
    db_data = db.query(File).all()
    return file_data, db_data


@app.put("/file/{file_name}")
async def update_file_name(file_id : int, file_name: str, db:db_dependency):
    file_model = db.query(File).filter(File.id == file_id).first()
    if file_model is None:
        raise HTTPException(status_code=404, detail='File not found')
    
    file_model.file_name = file_name
    
    # db.add(file_model)
    db.commit()
    update_filename = db.query(File).filter(File.id == file_id).first()
    return update_filename




@app.delete("/file/{file_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id : int, file_name: str, db:db_dependency):
    file_model = db.query(File).filter(File.id == file_id).first()
    if file_model is None:
        raise HTTPException(status_code=404, detail='File not found')
    
    db.query(File).filter(File.id == file_id).delete()
    db. commit()

















# @app.get("/files/{file_name}")
# async def read_file(file_name: str, db: db_dependency):
#     file_path = os.path.join(path, "Files/Music.txt")
#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type="text/html", filename="Music.txt")
#     file_model = db.query(File).filter(File.filename == file_name).first()

#     if file_model is not None:
#         return file_model
    
#     db.add(file_path)
#     db.add(file_model)
#     db.commit()

#     raise HTTPException(status_code=404, detail='File not found')



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3316)


