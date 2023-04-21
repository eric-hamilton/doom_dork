from configparser import ConfigParser
import json, os, sys

class ConfigParserWithAutoSave(ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = None
    
    def load(self, config_file):
        self.config_file = config_file
        super().read(config_file)

    def set(self, section, option, value):
        super().set(section, option, value)
        with open(self.config_file, 'w') as f:
            super().write(f)
            
            
parser = ConfigParserWithAutoSave()

warnings = []

class Config():
    def __init__(self, app):
        self.parser = parser
        self.app = app

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

def verify_iwads():
    doom_dir = parser.get("IWADS", "doom")
    doom_2_dir = parser.get("IWADS", "doom2")
    hexen_dir = parser.get("IWADS", "hexen")
    heretic_dir = parser.get("IWADS", "heretic")
    strife_dir = parser.get("IWADS", "strife")

    if os.path.isfile(doom_dir):
        return True
    elif os.path.isfile(doom_2_dir):
        return True
    elif os.path.isfile(hexen_dir):
        return True
    elif os.path.isfile(heretic_dir):
        return True
    elif os.path.isfile(strife_dir):
        return True
    else:
        return False
        
def create_default_config_file(root_dir):
    
    bin_dir = os.path.join(root_dir, "bin")
    engine_dir = os.path.join(root_dir, "engines")
    wad_dir = os.path.join(root_dir,"wads")
    
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
        
    config_file = os.path.join(bin_dir, "config.ini")
    parser.config_file = config_file
    
    # Define Defaults
    
    default_config = {
        'base_directory': root_dir,
        'engine_directory': engine_dir,
        'wad_directory': wad_dir,
        'use_steam_directory':False,
    }
    default_config = {k: str(v) for k, v in default_config.items()}
    
    default_iwads = {
        "doom":"",
        "doom2":"",
        "hexen":"",
        "heretic":"",
        "strife":"",
        "strife_voices":"",
    }
    default_iwads = {k: str(v) for k, v in default_iwads.items()}
    
    default_data = {
        "last_wad":"",
        "last_engine":"",
        "last_directory":".",
    }
    default_data = {k: str(v) for k, v in default_data.items()}

    if os.path.exists(config_file):
        # Verify Config File

        with open(config_file, 'r') as f:
            parser.read_file(f)

        if not parser.has_section("CONFIG"):
            parser.add_section("CONFIG")
        for key, value in default_config.items():
            if not parser.has_option("CONFIG", key):
                parser.set("CONFIG", key, value)
                
        if not parser.has_section("IWADS"):
            parser.add_section("IWADS")
        for key, value in default_iwads.items():
            if not parser.has_option("IWADS", key):
                parser.set("IWADS", key, value)
        
        if not parser.has_section("DATA"):
            parser.add_section("DATA")
        for key, value in default_data.items():
            if not parser.has_option("DATA", key):
                parser.set("DATA", key, value)
                
        with open(config_file, 'w') as f:
            parser.write(f)
        return
        
    
    for dir in [engine_dir, wad_dir]:
        if not os.path.exists(d):
            os.makedirs(d)

    parser["CONFIG"] = default_config
    parser["IWADS"] = default_iwads
    parser["DATA"] = default_data
    
    
    with open(config_file, 'w') as f:
        parser.write(f)
    
root_dir = create_root_directory()
create_default_config_file(root_dir)
if not verify_iwads():
    warnings.append("no_valid_iwads")