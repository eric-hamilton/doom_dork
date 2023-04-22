import struct
import omg
import os
import shutil
import subprocess
import concurrent.futures
import time
import json

import dork.web as web_utils
import dork.utils as dork_utils
from dork.models import Engine, WAD, WADFolder


class DoomDork:

    def __init__(self, app):
        self.app = app
        self.injected_iwad = None
        
    def update_local_engine(self, engine_dict):
        engine = self.app.db.query(Engine).get(engine_dict["engine_id"])
        engine.title = engine_dict["title"]
        engine.description = engine_dict["description"]
        engine.local = True
        engine.version = engine_dict["version"]
        self.app.db.commit()
        self.app.ui.handle_signal("engine_commit")

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
        
    
    def get_verified_iwad_path(self, iwad):
        iwad_path = self.app.config.parser.get("IWADS", iwad)
        if os.path.exists(iwad_path):
            return iwad_path
        else:
            return None
            
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
    
    def get_engine(self, engine_id):
        engine = self.app.db.query(Engine).get(engine_id)
        return engine
    
    def get_wad(self, wad_id):
        wad = self.app.db.query(WAD).get(wad_id)
        return wad
        
    def get_steam_wads(self):
        steam_dir = dork_utils.get_steam_directory()
        found_wads = dork_utils.find_wads_in_directory(steam_dir)
        print(found_wads)
        return
        for wad in found_wads:
            wad_class = WAD()
    
    def check_iwad(self, wad_path):
        wad_header = dork_utils.get_wad_header(wad_path)
        checksum = dork_utils.compute_checksum(wad_path)
        with open('dork/resources/iwad_hashes.json') as f:
            iwad_data = json.load(f)
        for iwad in iwad_data:
            if checksum == iwad["wad_md5"]:
                return True
        return False
        
        
    def get_iwads(self):
        iwad_list = []
        for iwad, path in self.app.config.parser.items("IWADS"):
            if os.path.exists(path):
                iwad_list.append(iwad)
        return iwad_list
            

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
    
    def on_subprocess_finished(self):
        if self.injected_iwad:
            os.remove(self.injected_iwad)
            self.injected_iwad = None
        
    
    def run_subprocess(self, engine_path, wad_path):
        subprocess.run([engine_path, wad_path])    
    
    def run_selected(self, engine_id, wad_id, iwad):
        engine_object = self.app.db.query(Engine).get(engine_id)
        engine_path = os.path.join(engine_object.folder_path, engine_object.executable)
        
        wad_object = self.app.db.query(WAD).get(wad_id)
        wad_path = wad_object.file_path
        iwad_path = self.get_verified_iwad_path(iwad)

        iwad_dest = os.path.join(engine_object.folder_path, os.path.basename(iwad_path))

        shutil.copyfile(iwad_path, iwad_dest)

        self.injected_iwad = iwad_dest
        
        self.app.config.parser.set("DATA", "last_wad", str(wad_id))
        self.app.config.parser.set("DATA", "last_engine", str(engine_id))
        self.app.config.parser.set("DATA", "last_iwad", str(iwad))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.run_subprocess, engine_path, wad_path)
            while not future.done():
                time.sleep(1)
            result = future.result()
            self.on_subprocess_finished()
            
