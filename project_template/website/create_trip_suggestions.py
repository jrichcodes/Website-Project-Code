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
        self.trips = []

world = {'Africa': {}, 'North America': {}, 'South America': {}, 'Asia': {}, 'Oceania': {}, 'Europe': {}}

Africa = continent("Africa")
North_America = continent("North America")
South_America = continent("South America")
Asia = continent("Asia")
Oceania = continent("Oceania")
Europe = continent("Europe")

names = []
images = []

# ------ Africa ------
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
    #curr_trip = trip(names[i], "website/static/images/suggestions/" + images[i][72::])
    curr_trip = trip(names[i], images[i][72::])
    Africa.trips.append(curr_trip)

for i in Africa.trips:
    world['Africa'][i.trip_name] = i.img

names.clear()
images.clear()

# ------North America------
req = requests.get('https://www.theevolista.com/usa-trip-ideas/')
finder = bs4.BeautifulSoup(req.text, 'lxml')

#Raw names
x = finder.find_all('h3')
y = finder.find_all('img',  loading="lazy")
# y = finder.find_all('figure',  class_="wp-block-image")


for i in x:
    if i.text[1] == '.':
        names.append(i.text[3::])
        # print(i.text[3::])
    elif i.text[2] == '.' and int(i.text[0:2]) < 41:
        names.append(i.text[4::])
        # print(i.text[4::])

count = 0
for i in y:
    if count >= 45:
        break
    if i["src"][0] == 'h' and count > 0 and count < 41:
        images.append(i["src"])
        count += 1
    elif i["src"][0] == 'h':
        count += 1

# Download all images
# for i in images:
#     req = requests.get(i, stream=True)
#     filename = "website/static/images/suggestions/" + i[55::]
#     filename = open(filename, 'wb')
#     req.raw.decode_content = True
#     shutil.copyfileobj(req.raw, filename)
#     filename.close
#     time.sleep(0.5)
#     print(filename)

# print(len(names))
# print(len(images))

for i in range(len(names)):
    curr_trip = trip(names[i], images[i][55::])
    North_America.trips.append(curr_trip)
    # print(names[i] + ": " + images[i][55::])

for i in North_America.trips:
    world['North America'][i.trip_name] = i.img

with open('website/static/json_files/suggestions.json', 'w') as json_file:
    json.dump(world, json_file, indent = 4)

