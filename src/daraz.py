import src.definitions
import src.downloader
import shelve
from collections import OrderedDict

def getDarazAllLinks():
    links = []
    linkshref = []
    f = shelve.open(src.definitions.darazLinksDB)
    try:
        soup = src.downloader.getPageSoup(src.definitions.darazBaseURL)
        if soup is None:
            print("error occured in daraz.py @src.downloader.getPageSoup")
        else:
            links = soup.select(src.definitions.darazLinkSelector)
            for link in links:
                linkshref.append(link['href'])
                # print(link['href'])
        # print(len(links))

        linkshref = list(OrderedDict.fromkeys(linkshref))
        f['allLinks'] = linkshref
    finally:
        f.close()

def getPageNumber():
    if not src.definitions.fileExists(src.definitions.darazLinksDB):
        getDarazAllLinks()
    else:
        print("skipping")
    f1 = shelve.open(src.definitions.darazLinksDB)
    f2 = shelve.open(src.definitions.darazLinksWithPageNumberDB)
    linksWithPage = []
    count = 0
    try:
        links = f1['allLinks']
        for link in links:
            count += 1
            print(count)
            pageNumberTags = []
            pageNumber = []
            soup = src.downloader.getPageSoup(link)
            if soup is None:
                print("error occured in daraz.py ->getPageNumber @src.downloader.getPageSoup")
            else:
                pageNumberTags = soup.select(src.definitions.darazPageNumberSelector)
            for tag in pageNumberTags:
                pageNumber.append(tag['title'])
            if len(pageNumber) == 0:
                linksWithPage.append({'link': link, 'pageNumber': 1})
            else:
                linksWithPage.append({'link': link, 'pageNumber': pageNumber[len(pageNumber)-2]})
        f2['linksPage'] = linksWithPage
    finally:
        f1.close()
        f2.close()

def getAllItems():
    if not src.definitions.fileExists(src.definitions.darazLinksDB):
        getDarazAllLinks()
    else:
        print("skipping getDarazAllLinks()")
    if not src.definitions.fileExists(src.definitions.darazLinksWithPageNumberDB):
        getPageNumber()
    else:
        print("skipping getPageNumber()")

    f1 = shelve.open(src.definitions.darazLinksWithPageNumberDB)
    f2 = shelve.open(src.definitions.darazAllItemsDB)

    try:
        dicts = f1['linksPage']
        count = 0
        for dic in dicts:
            count += 1
            # **************temp code*****
            if count <= 162:
                continue
            # ************temp code***********
            link = dic['link']
            print(count, link)
            pageNumber = dic['pageNumber']
            allItems = []
            for i in range(int(pageNumber)):
                print(i)
                soup = src.downloader.getPageSoup(link + "?page=" + str(i+1))
                if soup is None:
                    print("error occured in daraz.py -> getAllItems() @src.downloader.getPageSoup")
                else:
                    itemlinks = soup.select(src.definitions.darazItemLinkSelector)
                    imageSRCs = soup.select(src.definitions.darazImageSrcSelector)
                    titles = soup.select(src.definitions.darazTitleSelector)
                    brands = soup.select(src.definitions.darazBrandSelector)
                    rawprices = soup.select(src.definitions.darazPriceSelector)
                    prices = []
                    for j in range(0, len(rawprices), 2):
                        prices.append(rawprices[j].find(dir="ltr").text)
                for item,image,title,brand,price in zip(itemlinks,imageSRCs,titles,brands,prices):
                    allItems.append(src.definitions.Item(imgSrc=image['src'],
                                                         title=title.text,
                                                         price=price,
                                                         itemLink=item['href'],
                                                         vendor="daraz",
                                                         brand=brand.text.split('&')[0]))
            f2[link] = allItems

    finally:
        f1.close()
        f2.close()

def adjustBrands():

    # needed only once.......probably dont need it anymore

    file = shelve.open(src.definitions.darazAllItemsDB)
    try:
        for key in file:
            items = file[key]
            for item in items:
                item.brand = item.brand.split('&')[0]

        # file.sync()
    finally:
        file.close()

def deleteDuplicateInAllLinks():

    # needed only once.......probably dont need it anymore

    file = shelve.open(src.definitions.darazLinksDB)
    try:
        links = file['allLinks']
        links = list(OrderedDict.fromkeys(links))
        file['allLinks'] = links
    finally:
        file.close()


# getDarazAllLinks()
# getPageNumber()
# getAllItems()
# adjustBrands()
# deleteDuplicateInAllLinks()