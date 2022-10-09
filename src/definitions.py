import os, shelve

imagesHome = "E:\\online-shopping\\images\\"
priyoshopBaseURL = "http://www.priyoshop.com/"

priyoshopSublinkSelector = 'ul.sublist li a.with-subcategories'
priyoshopFinallinkSelector = 'ul.sublist li a'
pageNumberSelector = "div.pager ul li.last-page a"

imageSelector = 'div.product-item div.picture a img'
priceSelector = 'div.product-item span.price.actual-price'
descriptionSelector = 'div.product-item div.details div.add-info div.description'
itemLinkSelector = 'div.product-item div.details h2.product-title a'

priyoshopFinalLinkDB = 'C:\\Python_Projects\\OnlineShopping\\files\\priyoshop\\links.db'
priyoshopLinksWithPage = 'C:\\Python_Projects\\OnlineShopping\\files\\priyoshop\\linkswithpage.db'
priyoshopAllItems = 'C:\\Python_Projects\\OnlineShopping\\files\\priyoshop\\allitems.db'

priyoshopMultiPageUrl = "?pagenumber="
priyoshopAllInOnePage = ""

darazBaseURL = "https://www.daraz.com.bd/"
darazLinkSelector = 'nav.menu.-flyout ul.menu-items a.subcategory'
darazPageNumberSelector = "ul.osh-pagination.-horizontal li.item a"

darazItemLinkSelector = "section.products div.sku.-gallery a.link"
darazImageSrcSelector = darazItemLinkSelector + " " + "div noscript img.image"
darazBrandSelector = darazItemLinkSelector + " " + "h2.title span.brand"
darazTitleSelector = darazItemLinkSelector + " " + "h2.title span.name"
darazPriceSelector = darazItemLinkSelector + " " + "div span.price-box span.price"

darazLinksDB = "C:\\Python_Projects\\OnlineShopping\\files\\daraz\\links.db"
darazLinksWithPageNumberDB = "C:\\Python_Projects\\OnlineShopping\\files\\daraz\\linkswithpage.db"
darazAllItemsDB = "C:\\Python_Projects\\OnlineShopping\\files\\daraz\\allitems.db"

ajkerdealBaseURL = "https://ajkerdeal.com/allcategories.aspx"
ajkerdealLinkSelector = "section div div div h4 a"

bdhaatBaseURL = "http://www.bdhaat.com/"
bdhaatLinkSelector = ["li.level0 a", "li.level1 a", "li.level2 a", "li.level3 a"]
bdhaatLinkEliminator = ["li.level0.parent a", "li.level1.parent a",
                        "li.level2.parent a", "li.level3.parent a"]
bdhaatPagesofLinkSelector = "div.toolbar-bottom div.pager p.amount"

bdhaatItemLinkSelector = "li.item a.product-image"
bdhaatImgSrcSelector = bdhaatItemLinkSelector + " " + "img"
bdhaatPriceSelector = "li.item div.actions div.priceContainer div.price-box"
bdhaatPriceSelector2 = "li.item div.actions div.priceContainer div.price-box p.special-price span.price"

bdhaatLinksDB = "C:\\Python_Projects\\OnlineShopping\\files\\bdhaat\\links.db"
bdhaatPageNoDB = "C:\\Python_Projects\\OnlineShopping\\files\\bdhaat\\linkswithpage.db"
bdhaatAllItemsDB = "C:\\Python_Projects\\OnlineShopping\\files\\bdhaat\\allitems.db"

class Item:
    def __init__(self, imgSrc="", title="", description="", price="",
                 itemLink="", vendor="priyoshop", imageName="", brand=""):
        self.imageSrc = imgSrc
        self.title = title
        self.description = description
        self.price = price
        self.itemLink = itemLink
        self.vendor = vendor
        self.imageName = imageName
        self.brand = brand


def fileExists(filename):
    extensions = [".bak", ".dat", ".dir"]
    fileExist = True
    for extension in extensions:
        fileExist = fileExist and os.path.isfile(filename + extension)
    return fileExist
