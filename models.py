
from database import Base
from sqlalchemy import Integer, String, Column, DateTime

class File(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    file_name = Column(String, unique=True)
    location = Column(String)


