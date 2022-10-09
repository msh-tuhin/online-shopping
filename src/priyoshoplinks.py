import src.downloader
import src.definitions
from collections import OrderedDict
import shelve


def getPriyoshopAllLinks():
    soup = src.downloader.getPageSoup(src.definitions.priyoshopBaseURL)

    if soup is None:
        print("error occured")
        return
    else:
        print("successful")
        subLinks = soup.select(src.definitions.priyoshopSublinkSelector)
        finalLinks = soup.select(src.definitions.priyoshopFinallinkSelector)

        subLinks_href = []
        finalLinks_href = []

        for link in subLinks:
            subLinks_href.append(link['href'][1:])

        for link in finalLinks:
            finalLinks_href.append(link['href'][1:])

        finalLinks_href = list(OrderedDict.fromkeys(finalLinks_href))
        subLinks_href = list(OrderedDict.fromkeys(subLinks_href))
        for link in finalLinks_href:
            if link in subLinks_href:
                finalLinks_href.remove(link)

        # using set might be an option
        # finalLinks_href = list(set(finalLinks_href) - set(subLinks_href))

        file = shelve.open(src.definitions.priyoshopFinalLinkDB)
        try:
            file['allLinks'] = finalLinks_href
        finally:
            file.close()
        print(len(subLinks_href))
        print(len(finalLinks_href))

def getPageNumber():
    file = shelve.open(src.definitions.priyoshopFinalLinkDB)
    try:
        allLinks = file['allLinks']
    finally:
        file.close()

    linkWithPages = []
    if allLinks is not None and len(allLinks) > 0:
        for link in allLinks:
            soup = src.downloader.getPageSoup(src.definitions.priyoshopBaseURL + link)
            if soup is None:
                print("error occured")
            else:
                pagerElement = soup.select(src.definitions.pageNumberSelector)
                # print(link)
                if len(pagerElement) > 0:
                    pageNumber = int(pagerElement[0]['href'].split('=').pop())
                    linkWithPages.append({'link': link, 'pageNumber': pageNumber})
                else:
                    linkWithPages.append({'link': link, 'pageNumber': 1})

        file = shelve.open(src.definitions.priyoshopLinksWithPage)
        try:
            file['linksPage'] = linkWithPages
        finally:
            file.close()

def getAllItems():
    file = shelve.open(src.definitions.priyoshopLinksWithPage)
    file2 = shelve.open(src.definitions.priyoshopAllItems)
    try:
        dicts = file['linksPage']
        for dic in dicts:
            link = dic['link']
            pageNumber = dic['pageNumber']

            #if pageNumber = 0 the loop will not be entered
            allItems = []
            for i in range(1, pageNumber+1):
                print(src.definitions.priyoshopBaseURL + link
                                      + src.definitions.priyoshopMultiPageUrl + str(i))
                soup = src.downloader.getPageSoup(src.definitions.priyoshopBaseURL + link
                                      + src.definitions.priyoshopMultiPageUrl + str(i))
                if soup is None:
                    print("error occured")
                else:
                    images = soup.select(src.definitions.imageSelector)
                    prices = soup.select(src.definitions.priceSelector)
                    descriptions = soup.select(src.definitions.descriptionSelector)
                    itemLinks = soup.select(src.definitions.itemLinkSelector)

                    for image,price,description,itemLink in zip(images,prices,descriptions,itemLinks):
                        print(image, price, description, itemLink)
                        allItems.append(src.definitions.Item(imgSrc=image['src'],
                                                             title=image['title'],
                                                             description=description.text,
                                                             itemLink=['href'],
                                                             price=price.text))
            file2[link] = allItems


    finally:
        file.close()
        file2.close()
