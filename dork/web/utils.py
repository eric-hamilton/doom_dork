import urllib.request
import requests
from bs4 import BeautifulSoup


def get_ftp_file(ftp_link, output_path):
    username = "dork"
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, ftp_link, username, '')
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(ftp_link, output_path)    
        
        
def get_rating_from_stars(star_list):
    star_images = {'qstarmidright.gif': 0.25, 
                       'emptyhalfstar.gif': 0.0, 
                       'qstarfarleft.gif': 0.25, 
                       'star.gif': 1, 
                       'halfstar.gif': 0.5, 
                       'emptyqstarfarright.gif': 0.0, 
                       'emptyqstarmidleft.gif': 0.0}
    star_rating = 0
    for img in star_list:
        if img['src'].split('/')[-1] in star_images:
            star_rating += star_images[img['src'].split('/')[-1]]      
    return star_rating

def get_soup_or_fail(url):
    url = "https://www.doomworld.com/idgames/" + url
    response = requests.get(url)
    if not response.ok:
        return False
    soup = BeautifulSoup(response.content, "html.parser")
    return soup
