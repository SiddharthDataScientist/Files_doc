
from database import Base
from sqlalchemy import Integer, String, Column, DateTime

class File(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True, autoincrement= True)
    date = Column(DateTime)
    file_name = Column(String)
    location = Column(String)


    # id = Column(Integer, primary_key=True, index=True)
    # date_ = Column(String)
    # filename = Column(String)

