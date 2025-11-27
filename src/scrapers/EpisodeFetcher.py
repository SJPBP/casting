from WebScaper import WebScaper
import re

class EpisodeFetcher:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def get_episode(self):
        
        episode = {}

        episode["date"] = self.extract_date()
        episode["episodeTitle"] = self.extract_title()
        episode["thumbnail"] = self.extract_thumbnail()
        episode["contentUrl"] = self.extract_content_url()

        return episode

    
    def extract_date(self):
        xpath = '//li[@class="active"]'
        attr = 'text()'

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_title(self):
        xpath = '//h4[@class="subheading"]'
        attr = 'text()'
            
        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_thumbnail(self):
        xpath = '//figure[@class="episodethumb"]/img'
        attr = '@src'

        return self.webScraper.find(xpath=xpath, attr=attr)

    
    def extract_content_url(self):
        xpath = '//div[@id="video_player"]//following-sibling::script[@type="text/javascript"]'
        attr = 'text()'

        source = self.webScraper.find(xpath=xpath, attr=attr)

        pattern = r"\"(https?://[^\"]+)\""
        url = (re.search(pattern, source)).group(1)

        return url
