from gettext import find
import requests, bs4, re

class trip:
    trip_name = None
    img = None
    description = None

class continent:
    name = None
    trips = []

    def __init__(self, name):
        self.name = name

Africa = continent("Africa")
North_America = continent("North America")
South_America = continent("South America")
Asia = continent("Asia")
Oceania = continent("Oceania")
Europe = continent("Europe")

names = []
images = []

#Africa
req = requests.get('https://www.planetware.com/africa/best-places-to-visit-saf-1-36.htm')
finder = bs4.BeautifulSoup(req.text, 'lxml')

x = finder.find_all('h2', class_="sitename")
y = finder.find_all('img', class_='wpimg')

#Gets all the names in proper format
for i in range(len(x)):
    if x[i].text[2] == ' ':
        names.append(x[i].text[3::])
    elif x[i].text[3] == ' ':
        names.append(x[i].text[4::])
