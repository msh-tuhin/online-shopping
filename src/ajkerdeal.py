import src.downloader
import src.definitions
import requests

soup = src.downloader.getPageSoup(src.definitions.ajkerdealBaseURL)
allLinks = soup.select(src.definitions.ajkerdealLinkSelector)
linksHref = [link['href'] for link in allLinks]

for link in linksHref:
    print(link)

# response = requests.post("https://ajkerdeal.com/en/CategoryProduct.aspx/FirstComeFirstServe")
# print(response.content)

