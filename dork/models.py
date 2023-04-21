from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from dork.utils import convert_bytes
import os

Base = declarative_base()

class ToJson():
    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
        
class Engine(Base):
    __tablename__ = 'engines'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    executable = Column(String)
    folder_path = Column(String)
    version = Column(String)
    local = Column(Boolean)
    favorite = Column(Boolean, default=False)
    
    
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
    size_bytes = Column(Integer)
    credits = Column(String)
    base = Column(String)
    build_time = Column(String)
    editors_used = Column(String)
    bugs = Column(String)
    rating = Column(String)
    rating_count = Column(String)
    my_rating = Column(Integer)
    favorite = Column(Boolean, default=False)
    hidden = Column(Boolean, default=False)
    last_played = Column(Date)
    local = Column(Boolean)
    is_iwad = Column(Boolean, default=False)
    
    def init_from_local_filepath(self, file_path):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.title = self.filename
        self.size_bytes = os.path.getsize(file_path)
        self.size = convert_bytes(self.size_bytes)
        self.local = True
        
        

class WADFolder(Base):
    __tablename__ = "wadfolders"
    
    id = Column(Integer, primary_key=True)
    folder_name = Column(String)
    folder_path = Column(String)
    recursive = Column(Boolean, default=True)