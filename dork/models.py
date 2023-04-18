from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ToJson():
    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
        
class Engine(Base):
    __tablename__ = 'engines'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    executable = Column(String)
    folder_path = Column(String)
    version = Column(String)
    
class WAD(Base):
    __tablename__ = 'wads'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    date = Column(String)
    filename = Column(String)
    file_path = Column(String, unique=True)
    size = Column(String)
    credits = Column(String)
    base = Column(String)
    build_time = Column(String)
    editors_used = Column(String)
    bugs = Column(String)
    rating = Column(String)
    rating_count = Column(String)

class WADFolder(Base):
    __tablename__ = "wadfolders"
    
    id = Column(Integer, primary_key=True)
    folder_name = Column(String)
    folder_path = Column(String)
    recursive = Column(Boolean, default=True)