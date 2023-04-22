from bs4 import BeautifulSoup
import requests

class DoomWorldWADListing:
    def __init__(self, listing_element):
        self.name_element = listing_element.find("td", class_="wadlisting_name")
        self.title, self.rating, self.link, self.is_level, self.iwad = self.strip_name_element(self.name_element)
        self.description = listing_element.find("td", class_="wadlisting_description").text.strip()
        labels = listing_element.find_all("td", class_="wadlisting_label")
        fields = listing_element.find_all("td", class_="wadlisting_field")
        data_dict = dict(zip([label.text.lower().strip(":") for label in labels], [field.text for field in fields]))
        
        self.filename = data_dict.get("filename")
        self.date = data_dict.get("date")
        self.size = data_dict.get("size")
        self.author = data_dict.get("author")
        
    @staticmethod
    def strip_name_element(name_element):
        star_images = {'qstarmidright.gif': 0.25, 
                       'emptyhalfstar.gif': 0.0, 
                       'qstarfarleft.gif': 0.25, 
                       'star.gif': 1, 
                       'halfstar.gif': 0.5, 
                       'emptyqstarfarright.gif': 0.0, 
                       'emptyqstarmidleft.gif': 0.0}
        name = name_element.find("a").text.strip()
        link = name_element.find('a').get("href")
        path_list = link.split("/")
        if path_list[0] == "levels":
            is_level = True
            iwad = path_list[1]
        else:
            is_level = False
            iwad=None
        
        star_rating = 0
        for img in name_element.find_all('img', src=True):
            if img['src'].split('/')[-1] in star_images:
                star_rating += star_images[img['src'].split('/')[-1]]
        return name, star_rating, link, is_level, iwad
        
    def __repr__(self):
        return f'"{self.title}" by {self.author}'
        
def get_doomworld_listings_date(level_count=25):
    listing_objects = []
    page_number = 1
    running = True
    while running:
        url = f"https://www.doomworld.com/idgames//index.php?search&page={page_number}&field=filename&word=zip&sort=time&order=desc"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        page_listings = soup.find_all("table", class_="wadlisting")
        for listing in page_listings:
            listing_object = DoomWorldWADListing(listing)
            if listing_object.is_level:
                listing_objects.append(listing_object)
                if len(listing_objects) == level_count:
                    running = False
                    break
        page_number+=1
    return listing_objects

    
def get_doomworld_listings(number=25, topbottom="top", votes=50):
    form_url = "https://www.doomworld.com/idgames//index.php?top"

    data = {
        "number": number,
        "topbottom": topbottom,
        "votes": votes,
    }
    response = requests.post(form_url, data=data)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.find_all("table", class_="wadlisting")
    listing_objects = []
    for listing in listings:
        

        listing_object = DoomWorldWADListing(listing)
        listing_objects.append(listing_object)
    return listing_objects

