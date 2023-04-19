import winreg
import re, os, glob, math, hashlib


def strip_name_element(name_element):
    
    star_images = {'qstarmidright.gif': 0.25, 
               'emptyhalfstar.gif': 0.0, 
               'qstarfarleft.gif': 0.25, 
               'star.gif': 1, 
               'halfstar.gif': 0.5, 
               'emptyqstarfarright.gif': 0.0, 
               'emptyqstarmidleft.gif': 0.0}

    name = name_element.find("a").text.strip()
    star_rating=0
    for img in name_element.find_all('img', src=True):
        if img['src'].split('/')[-1] in star_images:
            star_rating += star_images[img['src'].split('/')[-1]]
    return name, star_rating
    

def get_registry_command(key_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, winreg.KEY_READ)
        command = winreg.QueryValue(key, None)
        winreg.CloseKey(key)
        return command
    except WindowsError:
        return False
        
def find_wads_in_directory(directory):
    wad_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.wad'):
                full_path = os.path.join(root, file)
                size_bytes = os.path.getsize(full_path)
                wad_files.append((full_path, size_bytes, file))
    return wad_files
    
def get_steam_directory():
    key_path = r"steam\\Shell\\Open\\Command"
    command = get_registry_command(key_path)
    if not command:
        return None
    match = re.search(r'"(.*?)"', command)
    if match:
        steam_exec = match.group(1)
        steam_dir = os.path.dirname(steam_exec)
        return steam_dir
    
    
    
def convert_bytes(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])       

def compute_checksum(file_path):
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Create an MD5 hash object
        md5 = hashlib.md5()

        # Read the file in chunks and update the hash object
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)

    # Return the hex digest of the hash
    return md5.hexdigest()
    
def get_wad_header(file_path):
    with open(file_path, "rb") as f: 
        wad_header = f.read(4).decode("utf-8")
        return wad_header
    
known_wads = {
    "Doom":{
        "size_bytes":12408292,
        
    }
}