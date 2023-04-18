from dork import config
from dork.ui import UI
from dork.dork import DoomDork
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dork.models import Base, Engine, WAD, WADFolder

db_engine = create_engine('sqlite:///dorkabase.db')
Session = sessionmaker(bind=db_engine)
db = Session()

Base.metadata.create_all(db_engine)


class App:
    
    def __init__(self):
        self.config = config.Config()
        self.dork = DoomDork()
        self.ui = UI(self)
        self.db = db
        
    def run(self):
        self.ui.launch()
        

def create_app():
    app = App()
    db.app = app
    return app
