import src.definitions
import requests
from bs4 import BeautifulSoup
import shelve, os

def getPageSoup(url):
    try:
        page = requests.get(url)
        if(page.status_code != 200):
            return None
        else:
            return BeautifulSoup(page.content, 'html.parser')
    except TimeoutError:
        getPageSoup(url)
    except :
        print("Something Wrong")

def downloadAllImages():
    file1 = shelve.open(src.definitions.priyoshopAllItems)
    file2 = shelve.open(src.definitions.priyoshopFinalLinkDB)
    try:
        links = file2['allLinks']
        for link in links:
            items = file1[link]
            location = src.definitions.imagesHome + link
            os.mkdir(location)
            count = 0
            for item in items:
                rawImage = requests.get(item.imageSrc)
                count +=1
                print(count)
                imageName = item.imageSrc.split('/').pop().split('.')[0]
                with open(location + "\\" + imageName + ".jpeg", 'wb') as f:
                    for chunk in rawImage:
                        f.write(chunk)

    finally:
        file1.close()
        file2.close()
