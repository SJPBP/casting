from EpisodePageScraper import EpisodePageScraper

filePath = "/home/fake/Documents/Itti Si Khushi - Main Page.html"
epps = EpisodePageScraper(pageUrl="https://apnetv.xyz/Hindi-Serial/Itti-Si-Khushi")

print(epps.get_episode("18th November 2025"))
