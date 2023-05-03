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
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def get_files():
    ## Declare th folder name here
    ## Get the filenames here
    # declare the date
    ##Insert into the table with all the above data
    return "files"

@app.get("/get_files")
async def read_all_file_names(folder_name:str):
    folder_path = os.path.expanduser("~/Desktop")+ "/" + folder_name
    files = os.listdir(folder_path)
    return {"files":files}



@app.get("/read_file")
async def read_file(db:db_dependency):
    now = datetime.now()
    filename = "MP3-1.mp3"
    location = os.path.abspath(filename)
    existing_file = db.query(File).filter(File.file_name == filename).first()
    # if existing_file:
    #     existing_file.location = location
    #     existing_file.date = now
    #     db.commit()
    #     db_data = db.query(File).all()
    #     return existing_file, db_data
    # else:
    #     file_data =  File(file_name = filename,location = location, date = now)
    #     db.add(file_data)
    #     db.commit()
    #     db_data = db.query(File).all()
    #     print(db_data)
    #     return file_data, db_data
    return existing_file

    
    
@app.get("/read_files")
async def read_file(db:db_dependency):
    now = datetime.now()
    filename = "MP3-2.mp3"
    location = os.path.abspath(filename)

    file_data =  File(file_name = filename, location = location, date = now)
    return file_data
    # db.add(file_data)
    # db.commit()
    # db_data = db.query(File).all()
    # # return file_data, db_data
    # # return db_data


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

@app.put("/files/{file_name}")
async def update_file_name(filename: str, db: db_dependency, file_request: FileRequest):
    file_model = db.query(File).filter(File.file_name == filename).first()

    file_model.file_name = file_request.file_name

    # db.add(file_model)
    db.commit()







@app.delete("/file/{file_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id : int, file_name: str, db:db_dependency):
    file_model = db.query(File).filter(File.id == file_id).first()
    if file_model is None:
        raise HTTPException(status_code=404, detail='File not found')
    
    db.query(File).filter(File.id == file_id).delete()
    db. commit()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3316)


