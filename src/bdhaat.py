import src.definitions as defs
import src.downloader
from collections import OrderedDict
import shelve, math

def getAllLinks():

    links = []
    elimlink = []
    f = shelve.open(src.definitions.bdhaatLinksDB)
    try:
        soup = src.downloader.getPageSoup(defs.bdhaatBaseURL)
        if soup is None:
            print("error occured in bdhaat.py @src.downloader.getPageSoup")
        else:
            for selector in defs.bdhaatLinkSelector:
                tags = soup.select(selector)
                for tag in tags:
                    links.append(tag['href'])
            for eliminator in defs.bdhaatLinkEliminator:
                tags = soup.select(eliminator)
                for tag in tags:
                    elimlink.append(tag['href'])

            for link in elimlink:
                if link in links:
                    links.remove(link)
            links = list(OrderedDict.fromkeys(links))
            # for link in links:
            #     print(link)
            # print(len(links))
            f['allLinks'] = links

    finally:
        f.close()

def getAllPages():
    file1 = shelve.open(defs.bdhaatLinksDB)
    file2 = shelve.open(defs.bdhaatPageNoDB)
    try:
        linkspage = []
        links = file1['allLinks']
        for link in links:
            print(link, end=" ")
            soup = src.downloader.getPageSoup(link)
            if soup is None:
                print("error occured in bdhaat.py/getAllItems() @src.downloader.getPageSoup()")
            else:
                pages = soup.select(defs.bdhaatPagesofLinkSelector)
                if len(pages) == 0:
                    val = 1
                else:
                    li = pages[0].text.split(' ')
                    for i in li:
                        if not i.isdigit():
                            li.remove(i)
                    val = math.ceil(int(li.pop())/9)
                print(val)
                linkspage.append({'link': link, 'pageNumber': val})
        print(len(linkspage))
        file2['linksPage'] = linkspage
    finally:
        file1.close()
        file2.close()

def getAllItems():
    file1 = shelve.open(src.definitions.bdhaatPageNoDB)
    file2 = shelve.open(src.definitions.bdhaatAllItemsDB)
    try:
        dicts = file1['linksPage']
        for dic in dicts:
            allitems = []
            link = dic['link']
            pagenumber = dic['pageNumber']
            for i in range(pagenumber):
                prices = []
                print(link + "?p=" + str(i+1))
                soup = src.downloader.getPageSoup(link + "?p=" + str(i+1))
                if soup is None:
                    print("error occured in bdhaat/getAllItems() @src.downloader.getPageSoup")
                else:
                    linksntitle = soup.select(defs.bdhaatItemLinkSelector)
                    imagesrc = soup.select(defs.bdhaatImgSrcSelector)
                    tempprices = soup.select(defs.bdhaatPriceSelector)
                    for elem in tempprices:
                        child_elem = elem.select('p.special-price span.price')
                        if len(child_elem) == 0:
                            child_elem = elem.select('span.regular-price span.price')
                        prices.append(child_elem[0])
                    print(len(linksntitle), len(imagesrc), len(prices))
                    for lnt, imgsrc, price in zip(linksntitle, imagesrc, prices):
                        print(lnt['title'], price.text.strip()[1:])
                        allitems.append(defs.Item(imgSrc=imgsrc['src'], title=lnt['title'],
                                                vendor="bdhaat", itemLink=lnt['href'], price=price.text.strip()[1:]))
            print(link, " : ", len(allitems))
            file2[link] = allitems

    finally:
        file1.close()
        file2.close()

if __name__ == '__main__':
    if not src.definitions.fileExists(src.definitions.bdhaatLinksDB):
        src.bdhaat.getAllLinks()

    if not src.definitions.fileExists(src.definitions.bdhaatPageNoDB):
        src.bdhaat.getAllPages()

    if not src.definitions.fileExists(src.definitions.bdhaatAllItemsDB):
        src.bdhaat.getAllItems()
    # getAllLinks()
    # getAllPages()
    # getAllItems()

