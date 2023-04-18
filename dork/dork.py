import struct
import omg
import os
import subprocess
import dork.web as web_utils
import dork.utils as dork_utils


class DoomDork:
    def __init__(self):
        #self.get_steam_wads()
        
        self.engines = []
        
    
                
    def get_steam_wads(self):
        steam_dir = dork_utils.get_steam_directory()
        found_wads = dork_utils.find_wads_in_directory(steam_dir)
        print(found_wads)
        
        
    def get_wads_in_folder(self, folder_path):

        wad_dict = {}
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".wad"): 
                    full_path = os.path.join(root, file)
                    wad_dict[file]=full_path
                    
        return wad_dict
        
    def analyze_wad(self, wad_path):
        print(wad_path)
        # Open the WAD file in binary mode
        wad = omg.WAD(wad_path)
        for x in wad.structure:
            print(x)
    
    def run_selected(self, engine_path, wad_path):
        subprocess.run([engine_path, wad_path])
    

