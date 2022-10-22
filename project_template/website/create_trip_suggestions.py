from gettext import find
import requests, bs4, re, shutil, time, json, os

names = []
images = []

world = {'Africa': {}, 'North America': {}, 'South America': {}, 'Asia': {}, 'Oceania': {}, 'Europe': {}}

def create_images(images, name_index):
    for i in images:
        req = requests.get(i, stream=True)
        filename = "website/static/images/suggestions/" + i[name_index::]
        filename = open(filename, 'wb')
        req.raw.decode_content = True
        shutil.copyfileobj(req.raw, filename)
        filename.close
        print(filename)
        time.sleep(0.5)

def create_africa(world, images, names):
    # ------ Africa ------ #
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
    
    #Download images
    # create_images(images, 72)
    
    for i in range(len(x)):
        world['Africa'][names[i]] = images[i][72::]
    
    
    names.clear()
    images.clear()

def create_north_america(world, images, names):
    # ------North America------- #
    images.clear()
    names.clear()

    req = requests.get('https://www.theevolista.com/usa-trip-ideas/')
    finder = bs4.BeautifulSoup(req.text, 'lxml')
    
    #Raw names
    x = finder.find_all('h3')
    y = finder.find_all('img',  loading="lazy")
    # y = finder.find_all('figure',  class_="wp-block-image")
    
    
    for i in x:
        if i.text[1] == '.':
            names.append(i.text[3::])
        elif i.text[2] == '.' and int(i.text[0:2]) < 41:
            names.append(i.text[4::])
    
    count = 0
    for i in y:
        if count >= 45:
            break
        if i["src"][0] == 'h' and count > 0 and count < 41:
            images.append(i["src"])
            count += 1
        elif i["src"][0] == 'h':
            count += 1
    
    #Download images
    #create_images(images, 55)
    
    for i in range(len(names)):
        world['North America'][names[i]] = images[i][55::]
    


def create_south_america(world, images, names):
    # ------South America------- #
    images.clear()
    names.clear()

    req = requests.get('https://www.jetsetter.com/magazine/life-changing-trips-to-take-in-south-america/')
    finder = bs4.BeautifulSoup(req.text, 'lxml')
    
    x = finder.find_all('h2', class_ = "heading")
    y = finder.find_all('div', class_ = 'img-fit__image-contain')
    
    
    #Get names
    for i in x:
        names.append(i.text.strip())
    
    #Get images
    for i in y:
        if len(images) == 10:
            break
    
        tag = i.find('img')
        if tag["sizes"].find('768') == -1:
            images.append(tag["src"])
    
    # Download all images
    # create_images(images, 51)
    
    for i in range(len(names)):
        world['South America'][names[i]] = images[i][51::]
    

def create_asia(world, images, names):
    #-----Asia-----
    images.clear()
    names.clear()

    req = requests.get('https://globalcastaway.com/southeast-asia-bucket-list/')
    finder = bs4.BeautifulSoup(req.text, 'lxml')
    
    
    x = finder.find_all('h3')
    y = finder.find_all('img')
    
    for i in x:
        if i.find('span'):
            names.append(i.find('span').text)
    
    count = 0
    for i in y:
        if i["src"][0] == 'h':
            if count > 1 and count < 52:
                images.append(i["src"])
            count += 1
    
    # create_images(images, 54)
    
    for i in range(len(names)):
        world['Asia'][names[i]] = images[i][54::]
    



def create_oceania(world, images, names):
    #----Oceania----
    images.clear()
    names.clear()

    req = requests.get('https://www.joaoleitao.com/travel-oceania/')
    finder = bs4.BeautifulSoup(req.text, 'lxml')
    
    x = finder.find_all('h3', class_='title3')
    y = finder.find_all('img', loading='lazy')
    
    
    for i in x:
        if i.text[1] == '-':
            names.append(i.text[3::])
        elif i.text[2] == '-':
            names.append(i.text[4::])
    
    count = 0
    for i in y:
        if count > 0:
            images.append(i['src'])
        count += 1
    
    # create_images(images, 54)
    
    for i in range(len(names)):
        world['Oceania'][names[i]] = images[i][54::]

def create_europe(world, images, names):
    #----Europe----
    images.clear()
    names.clear()
    
    req = requests.get('https://www.secretatlastravel.com/explorers-club/travel-tips/best-places-in-europe-to-visit/')
    finder = bs4.BeautifulSoup(req.text, 'lxml')
    
    x = finder.find_all('span', class_='s1')
    y = finder.find_all('img', class_='vc_single_image-img')
    
    for i in x:
        if len(i.text) < 100 and len(i.text) > 3:
            string = i.text.split(" ", 1)[1]
            if string[0] == '.':
                names.append(string[1::])
            else:
                names.append(string)
    
    count = 0
    for i in y:
        if count % 2 == 0:
            images.append(i['data-src'])
        count += 1

    # create_images(images, 61)

    for i in range(len(names)):
        world['Europe'][names[i]] = images[i][61::]


create_africa(world, images, names)
create_north_america(world, images, names)
create_south_america(world, images, names)
create_asia(world, images, names)
create_oceania(world, images, names)
create_europe(world, images, names)


with open('website/static/json_files/suggestions.json', 'w') as json_file:
    json.dump(world, json_file, indent = 4)

