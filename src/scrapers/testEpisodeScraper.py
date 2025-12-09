from scrapers.EpisodeScraper import EpisodeScraper

filePath = "/home/fake/Documents/ApneTV_Home_Page.html"
filePath = "/home/fake/Documents/Sab-TV India Online _ Serials & Discussions.html"
filePath = "/home/fake/Documents/Itti Si Khushi 21st November.html"
filePath = "/home/fake/Documents/Itti Si Khushi - Main Page.html"
print(filePath)
cs = EpisodeScraper(filePath=filePath)
print(cs.shallow_search())
# print(cs.get_episode())
# eps = cs.get_episodes(1)
# print(eps)
#
# ep = eps["Episodes"]
# ep = ep[0]

# print(ep.get_date_in_mysql_format())
# print(ep.get_date_in_apnetv_format())
# print(ep.update_content_type())
# print(ep)
