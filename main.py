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


origins = ["*"]

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



@app.get("/")
async def update_table(db:db_dependency):
    location = location = os.path.expanduser("~/Desktop/Songs")
    date = datetime.now()
    list_files = db.query(File.file_name).filter(File.location == location).all()
    list_files = set([f[0] for f in list_files])
    for filename in os.listdir(location):
        if filename in list_files:
            continue
        else:
            new_file = File(file_name =filename, location = location, date =date)
            db.add(new_file)
    db.commit()


@app.put("/files/{update_file_name}",status_code=status.HTTP_204_NO_CONTENT)
async def update_file_name(file_id: int , db: db_dependency, filename: str):
    file_model = db.query(File).filter(File.id == file_id).first()

    file_model.file_name = filename

    db.commit()


@app.delete("/files/{delete_file}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_name: str, db:db_dependency, ):
    delete_file = db.query(File).filter(File.file_name == file_name).all()
    if delete_file is None:
        raise HTTPException(status_code=404, detail='File not found')
    
    for files in delete_file:
        db.delete(files)

    db. commit()






# @app.get("/read_files/{file_name}")
# async def file_name(Songs:str):
#     location = os.path.expanduser("~/Desktop") + "/" + Songs
#     file_name = os.listdir(location)
#     date = datetime.now()
#     file_info = {
#         "files": file_name,
#         "location": location,
#         "date" : date
#     }
#     return file_info




# 68:
# db_filename = db.query(File.file_name).filter(File.location == directory).all()




# @app.put("/files/{file_name}")
# async def file_name(file_name:str, db:db_dependency):
#     file_model = db.query(File).filter(File.file_name == file_name).first()
#     file_model.file_name = file_name
#     db.commit()
#     # update_file_name = db.query(File).filter(File.file_name==file_name).first()
#     # return





# @app.get("/read_file")
# async def read_file(db:db_dependency):
#     now = datetime.now()
#     filename = "MP3-1.mp3"
#     location = os.path.abspath(filename)
#     existing_file = db.query(File).filter(File.file_name == filename).first()
# #     # if existing_file:
#     #     existing_file.location = location
#     #     existing_file.date = now
#     #     db.commit()
#     #     db_data = db.query(File).all()
#     #     return existing_file, db_data
#     # else:
#     #     file_data =  File(file_name = filename,location = location, date = now)
#     #     db.add(file_data)
#     #     db.commit()
#     #     db_data = db.query(File).all()
#     #     print(db_data)
#     #     return file_data, db_data
#     return existing_file

    
    
# @app.get("/read_files")
# async def read_file(db:db_dependency):
#     now = datetime.now()
#     filename = "MP3-2.mp3"
#     location = os.path.abspath(filename)

#     file_data =  File(file_name = filename, location = location, date = now)
#     return file_data
# #     # db.add(file_data)
# #     # db.commit()
#     # db_data = db.query(File).all()
#     # # return file_data, db_data
#     # # return db_data


# @app.put("/file/{file_name}")
# async def update_file_name(file_id : int, file_name: str, db:db_dependency):
#     file_model = db.query(File).filter(File.id == file_id).first()
#     if file_model is None:
#         raise HTTPException(status_code=404, detail='File not found')
    
#     file_model.file_name = file_name
    
#     # db.add(file_model)
#     db.commit()
#     update_filename = db.query(File).filter(File.id == file_id).first()
#     return update_filename

# # @app.put("/files/{file_name}")
# # async def update_file_name(filename: str, db: db_dependency):
# #     file_model = db.query(File).filter(File.file_name == filename).first()

# #     file_model.file_name = filename

# #     # db.add(file_model)
# #     db.commit()




# @app.delete("/file/{file_name}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_file(file_id : int, file_name: str, db:db_dependency):
#     file_model = db.query(File).filter(File.id == file_id).first()
#     if file_model is None:
#         raise HTTPException(status_code=404, detail='File not found')
    
#     db.query(File).filter(File.id == file_id).delete()
#     db. commit()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3316)


