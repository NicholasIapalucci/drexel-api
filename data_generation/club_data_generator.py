from bs4 import BeautifulSoup
from urllib.request import urlopen
import re as regex
import json

def html(url):
    return BeautifulSoup(urlopen(url).read(), features = "html.parser")

# The website only shows so many upon initial page load, so the full file must be stored locally
clubs_html = BeautifulSoup(open("data_generation/pages/clubs.html").read(), features = "html.parser")
clubs = clubs_html.find_all("div", class_="MuiPaper-root MuiCard-root MuiPaper-elevation3 MuiPaper-rounded")

organizations = {}

for club_element in clubs:
    club_div = club_element.find("div").find("span").find("div").find("div")
    club_name = regex.sub(r"\s+", " ", club_div.find("div", attrs={"alt": None}).decode_contents()).strip()
    club_desc = regex.sub(r"\s+", " ", club_div.find("p").decode_contents()).strip()
    link = club_element.parent["href"]

    organizations[club_name] = {
        "brief description": club_desc,
    }

open("src/data/organizations.json", "w").write(json.dumps(organizations, indent=4))

