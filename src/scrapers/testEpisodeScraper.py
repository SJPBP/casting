from EpisodeScraper import EpisodeScraper
filePath = "/home/fake/Documents/ApneTV_Home_Page.html"
filePath = "/home/fake/Documents/Sab-TV India Online _ Serials & Discussions.html"
filePath = "/home/fake/Documents/Itti Si Khushi 21st November.html"
filePath = "/home/fake/Documents/Itti Si Khushi - Main Page.html"
print(filePath)
cs = EpisodeScraper(filePath=filePath)

# print(cs.get_episode())
print(cs.get_episodes())

