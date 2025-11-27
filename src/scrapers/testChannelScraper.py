from ChannelScraper import ChannelScraper
filePath = "/home/fake/Documents/ApneTV_Home_Page.html"

cs = ChannelScraper(filePath=filePath)

print(cs.get_channels())
print(cs.get_channel("Sony-TV"))

