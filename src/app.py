import src.priyoshoplinks
import src.definitions
import src.daraz
import src.bdhaat
import src.downloader
import os
import shelve

if not src.definitions.fileExists(src.definitions.priyoshopFinalLinkDB):
    src.priyoshoplinks.getPriyoshopAllLinks()

if not src.definitions.fileExists(src.definitions.priyoshopLinksWithPage):
    src.priyoshoplinks.getPageNumber()

if not src.definitions.fileExists(src.definitions.priyoshopAllItems):
    src.priyoshoplinks.getAllItems()

if not src.definitions.fileExists(src.definitions.darazLinksDB):
    src.daraz.getDarazAllLinks()

if not src.definitions.fileExists(src.definitions.darazLinksWithPageNumberDB):
    src.daraz.getPageNumber()

if not src.definitions.fileExists(src.definitions.darazAllItemsDB):
    src.daraz.getAllItems()

if not src.definitions.fileExists(src.definitions.bdhaatLinksDB):
    src.bdhaat.getAllLinks()

if not src.definitions.fileExists(src.definitions.bdhaatPageNoDB):
    src.bdhaat.getAllPages()

if not src.definitions.fileExists(src.definitions.bdhaatAllItemsDB):
    src.bdhaat.getAllItems()

# if not os.path.isdir(src.definitions.imagesHome):
#     src.downloader.downloadAllImages()

# src.downloader.downloadAllImages()


