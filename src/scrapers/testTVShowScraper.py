from classes.TVSHOW import TVSHOW
from scrapers.TVShowScraper import TVShowScraper

filePath = "/home/fake/Documents/Sab-TV India Online _ Serials & Discussions.html"

tv = TVShowScraper(filePath=filePath)

# print(tv.get_tv_shows())
print(tv.get_tv_show("Baalveer Season 5"))
