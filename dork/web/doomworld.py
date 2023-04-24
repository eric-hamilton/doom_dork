from dork.web import DoomWorldWADListing
from bs4 import BeautifulSoup
import requests
import random

base_url = "https://www.doomworld.com/idgames/"
def get_random_wads(games, quota=10):
    listing_objects = []
    level_urls = [
        "levels/<GAME>/0-9/",
        "levels/<GAME>/a-c/",
        "levels/<GAME>/d-f/",
        "levels/<GAME>/g-i/",
        "levels/<GAME>/j-l/",
        "levels/<GAME>/m-o/",
        "levels/<GAME>/megawads/",
        "levels/<GAME>/p-r/",
        "levels/<GAME>/s-u/",
        "levels/<GAME>/v-z/",
    ]
    searching = True
    count = 0
    while searching:
        game = random.choice(games)
        sub_url = random.choice(level_urls).replace("<GAME>", game)
        url = base_url+sub_url
        page_listings = get_page_listings(url)
        if page_listings:
            listing = random.choice(page_listings)
            listing_object = DoomWorldWADListing(listing)
            listing_objects.append(listing_object)
            if len(listing_objects) >= quota or count > 100:
                searching = False
        count+=1
    return listing_objects
        
        
        
def get_page_listings(doomworld_url):
    response = requests.get(doomworld_url)
    
    if not response.ok:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all("table", class_="wadlisting")
    return listings
    
    
    
    