import struct
import omg
import os
import subprocess
import dork.web as web_utils
import dork.utils as dork_utils
from dork.models import Engine, WAD, WADFolder

class DoomDork:

    def __init__(self, app):
        self.app = app

    def add_local_engine(self, engine_dict):
        new_engine = Engine()
        engine_path = engine_dict["engine_path"]
        new_engine.title = engine_dict["title"]
        new_engine.description = engine_dict["description"]
        new_engine.executable = os.path.basename(engine_path)
        new_engine.folder_path = os.path.dirname(engine_path)
        new_engine.local = True
        new_engine.version = engine_dict["version"]
        self.app.db.add(new_engine)
        self.app.db.commit()
        self.app.ui.handle_signal("engine_commit")
        
        
    def get_local_engines(self):
        engines = self.app.db.query(Engine).filter(Engine.local == True)
        return engines
    
    def get_local_wads(self):
        wads = self.app.db.query(WAD).filter(WAD.local == True)
        return wads
    
    def add_local_wads_from_folder(self, folder_path, add_folder=False, recursive=True):
        if add_folder:
            new_wad_folder = WADFolder()
            new_wad_folder.folder_name = os.path.basename(os.path.normpath(folder_path))
            new_wad_folder.folder_path = folder_path
            new_wad_folder.recursive = recursive
            self.app.db.add(new_wad_folder)
            
        wad_list = self.get_wads_in_folder(folder_path)
        for wad in wad_list:
            self.add_local_wad(wad)
        self.app.db.commit()
        self.app.ui.handle_signal("wad_commit")
        
        
    def add_local_wad(self, wad_path):
        new_wad = WAD()
        new_wad.init_from_local_filepath(wad_path)
        self.app.db.add(new_wad)
    
    def get_all_wads(self):
        all_wads = self.app.db.query(WAD).all()
        return all_wads
        
    def get_all_engines(self):
        all_engines = self.app.db.query(Engine).all()
        return all_engines
        
    def get_steam_wads(self):
        steam_dir = dork_utils.get_steam_directory()
        found_wads = dork_utils.find_wads_in_directory(steam_dir)
        print(found_wads)
        return
        for wad in found_wads:
            wad_class = WAD()
        
        
        
    def get_wads_in_folder(self, folder_path):

        wad_list = []
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".wad"): 
                    full_path = os.path.join(root, file)
                    wad_list.append(full_path)
                    
        return wad_list
        
    def analyze_wad(self, wad_path):
        wad = omg.WAD(wad_path)
        for x in wad.structure:
            print(x)
    
    def run_selected(self, engine_id, wad_id):
        engine_object = self.app.db.query(Engine).get(engine_id)
        engine_path = os.path.join(engine_object.folder_path, engine_object.executable)
        
        wad_object = self.app.db.query(WAD).get(wad_id)
        wad_path = wad_object.file_path
        
        subprocess.run([engine_path, wad_path])
    

