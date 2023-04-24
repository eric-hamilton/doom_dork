from bs4 import BeautifulSoup
import requests
import re
import dork.web.utils as web_utils

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
        
        name = name_element.find("a").text.strip()
        link = name_element.find('a').get("href")
        path_list = link.split("/")
        if path_list[0] == "levels":
            is_level = True
            iwad = path_list[1]
        else:
            is_level = False
            iwad=None
        
        star_rating = web_utils.get_rating_from_stars(name_element.find_all('img', src=True))
        return name, star_rating, link, is_level, iwad
        
    def __repr__(self):
        return f'"{self.title}" by {self.author}'


class DoomWorldWADDetail:
    def __init__(self, soup_object):
        self.ftp_links = {}
        self.http_links = {}
        dl_table = soup_object.find("table", class_="download")
        dl_links = dl_table.find_all('a')
        self.base_iwad = None
        
        for link in dl_links:
            link_location = link.text.lower().split()[0]
            if not self.base_iwad:
                match = re.search(r'/levels/(\w+)/', link_location)
                if match:
                    self.base_iwad = match.group(1)
            link_url = link.get("href")
            if "ftp" in link.text.lower():
                self.ftp_links[link_location] = link_url
            else:
                if ".zip" in link_url:
                    self.http_links[link_location] = link_url
        
        info_table = soup_object.find("table", class_="filelist")
        file_dict = {}
        for row in info_table.find_all("tr"):
            cells = row.find_all("td")
            cell_title = cells[0].text.lower().strip(":")
            cell_value = cells[1].text.lstrip()
            if cell_title != "rating":
                # format doomworld's titles
                if cell_title == "build time":
                    cell_title = "build_time"
                elif cell_title == "editor(s) used":
                    cell_title = "editors_used"
                  
                file_dict[cell_title] = cell_value
            else:
                image_list = cells[1].find_all('img', src=True)
                file_dict["rating"] = web_utils.get_rating_from_stars(image_list)
        for k, v in file_dict.items():
            setattr(self, k, v)
    def __repr__(self):
        return f"{self.title} by {self.author}, size: {self.size}, rating: {self.rating}"
        
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

