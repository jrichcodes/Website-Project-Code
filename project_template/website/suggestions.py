from gettext import find
import requests, bs4, re, shutil, time, json

class trip:
    trip_name = None
    img = None
    #TODO Africa
    description = None

    def __init__(self, trip_name, img):
        self.trip_name = trip_name
        self.img = img

class continent:
    name = None
    trips = []

    def __init__(self, name):
        self.name = name

world = {'Africa': {}, 'North America': {}, 'South America': {}, 'Asia': {}, 'Oceania': {}, 'Europe': {}}

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

#Raw names
x = finder.find_all('h2', class_="sitename")
#Raw image links
y = finder.find_all('img', class_='wpimg')

#Gets all the names in proper format
for i in range(len(x)):
    if x[i].text[2] == ' ':
        names.append(x[i].text[3::])
    elif x[i].text[3] == ' ':
        names.append(x[i].text[4::])

for i in y:
    images.append("https://www.planetware.com" + i["src"])

# for i in images:
#     req = requests.get(i, stream=True)
#     filename = "website/static/images/suggestions/" + i[72::]
#     filename = open(filename, 'wb')
#     req.raw.decode_content = True
#     shutil.copyfileobj(req.raw, filename)
#     filename.close
#     time.sleep(0.5)

for i in range(len(x)):
    curr_trip = trip(names[i], "website/static/images/suggestions/" + images[i][72::])
    Africa.trips.append(curr_trip)

for i in Africa.trips:
    world['Africa'][i.trip_name] = i.img


with open('website/static/json_files/suggestions.json', 'w') as json_file:
    json.dump(world, json_file, indent = 4)

