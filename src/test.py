import shelve
import src.definitions

def testlinks(dbfile):
    file = shelve.open(dbfile)
    try:
        links = file['allLinks']
        for link in links:
            print(link)
        print("Number of Links: {}".format(len(links)))
    finally:
        file.close()

def testlinkswithpage(dbfile):
    file = shelve.open(dbfile)
    try:
        dicts = file['linksPage']
        for dic in dicts:
            print("{} has {} pages".format(dic['link'], dic['pageNumber']))

        print("Number of Links: {}".format(len(dicts)))
    finally:
        file.close()

def testallItems(linkDB, itemsDB):
    file1 = shelve.open(linkDB)
    file2 = shelve.open(itemsDB)
    f = open("C:\\Users\\Tuhin\\Desktop\\out.txt", "w")
    try:
        links = file1['allLinks']
        itemCount = 0
        linkCount = 0
        for link in links:
            linkCount += 1
            items = file2[link]
            for item in items:
                print(item.itemLink)
                f.write(item.imageSrc + "\n")
                itemCount += 1
        print("Number of links: {}".format(linkCount))
        print("Number of total items: {}".format(itemCount))
        f.close()
    finally:
        file1.close()
        file2.close()

if __name__ == '__main__':

    # tests for PRIYOSHOP

    # testlinks(src.definitions.priyoshopFinalLinkDB)
    # testlinkswithpage(src.definitions.priyoshopLinksWithPage)
    # testallItems(src.definitions.priyoshopFinalLinkDB, src.definitions.priyoshopAllItems)


    # tests for DARAZ

    # testlinks(src.definitions.darazLinksDB)
    # testlinkswithpage(src.definitions.darazLinksWithPageNumberDB)
    # testallItems(src.definitions.darazLinksDB, src.definitions.darazAllItemsDB)

    #tests for BDHAAT
    # testlinks(src.definitions.bdhaatLinksDB)
    # testlinkswithpage(src.definitions.bdhaatPageNoDB)
    testallItems(src.definitions.bdhaatLinksDB, src.definitions.bdhaatAllItemsDB)
