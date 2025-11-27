from WebScaper import WebScaper
from CLASS.TVSHOW import TVSHOW
import re

class TVShowFetcher:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def get_tv_show(self):
        xpath = "/html/body"
        self.soup = self.webScraper.find(xpath=xpath)

        name = self.extract_name()
        thumbnail = self.extract_icon()
        totalEpisodes = self.extract_total_episodes()
        description = self.extract_description()
        channel = self.extract_channel_name()

        tvShow = TVSHOW(channel=channel, name=name, 
                        thumbnail=thumbnail, totalEpisodes=totalEpisodes, 
                        description=description)

        return tvShow
    
    def extract_name(self):
        xpath = '//div[@class="cont-img"]/figure/img'
        attr = '@alt'

        return self.webScraper.find(xpath=xpath, attr=attr)
    
    def extract_icon(self):
        xpath = '//div[@class="cont-img"]/figure/img'
        attr = '@src'

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_total_episodes(self):
        xpath = 'count(//select[@id="oneclick-episode"]/option)'

        result = int(self.webScraper.runFunction(xpath=xpath))
        return result
    
    def extract_channel_name(self):
        xpath = '//h5[@class="contentp-channel-data"]/a'
        attr = 'text()'
        
        return self.webScraper.find(xpath=xpath, attr=attr)

    
    def extract_description(self):
        xpath = '//div[@class="story-section"]'
        attr = "text()"

        return self.webScraper.find(xpath=xpath, attr=attr)


