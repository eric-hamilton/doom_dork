import configparser
import json, os, sys
config = configparser.ConfigParser()

class Config():
    def __init__(self):
        self.config = config
    
    def get_dork_path(self, path_string):
        # path string example "resources/icons/square.svg"
        # This should be changed to reflect the new bin directory
        
        path_list = path_string.split("/")
        if "dork" not in path_list:
            path_list.insert(0, "dork")
        root_file_path = os.path.abspath(sys.argv[0])
        root_dir_path = os.path.dirname(root_file_path)
        output_path_string = os.path.join(root_dir_path, *path_list)
        return output_path_string
        
def create_root_directory():
    roaming_folder = os.getenv("APPDATA")
    root_directory = os.path.join(roaming_folder, "Doom Dork")
    os.makedirs(root_directory, exist_ok=True)
    return root_directory

def create_defaults(root_dir):
    
    bin_dir = os.path.join(root_dir, "bin")
    
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
        
    config_file = os.path.join(bin_dir, "config.ini")
    
    if os.path.exists(config_file):
        return
        
    engine_dir = os.path.join(root_dir, "engines")
    wad_dir = os.path.join(root_dir,"wads")
    for dir in [engine_dir, wad_dir]:
        if not os.path.exists(d):
            os.makedirs(d)
    default_config = {
        'base_directory': root_dir,
        'engine_directory': engine_dir,
        'wad_directory': wad_dir,
    }
    config['CONFIG'] = default_config
    with open(config_file, 'w') as f:
        config.write(f)
    
root_dir = create_root_directory()
create_defaults(root_dir)
