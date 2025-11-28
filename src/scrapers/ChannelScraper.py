from scrapers.WebScaper import WebScaper

class ChannelScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def get_channels(self):
        """
        Return list of channels
        """
        xpath = '//div[@class="channel-title-logo"]'
        self.soup = self.webScraper.find_all(xpath)

        # channels = {}
        # channels["Channels"] = []
        channels = []

        for channel_soup in self.soup:
            self.soup = channel_soup
            channel = {}
            channel["Channel"] = {}

            channel["Channel"]["ChannelName"] = self.extract_name()
            channel["Channel"]["channelIcon"] = self.extract_icon()
            channel["Channel"]["channelUrl"] = self.extract_page_url()

            channels.append(channel)


        return channels


    def get_channel(self, name: str):
        xpath = f'//h2[text()="{name}"]'
        self.soup = self.webScraper.find(xpath)
       
        channels = []
        channel = {}

        channel["ChannelName"] = self.extract_name(singleSearch=True)
        channel["channelIcon"] = self.extract_icon(singleSearch=True)
        channel["channelUrl"] = self.extract_page_url(singleSearch=True)

        channels.append(channel)


        return channels

    
    def extract_name(self, singleSearch: bool = False):
        xpath = '//figure/img'
        attr = '@alt'

        if singleSearch:
            backtrack = '/..'
            xpath = backtrack + xpath
            
        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)

    def extract_icon(self, singleSearch: bool = False):
        xpath = '//figure/img'
        attr = '@src'

        if singleSearch:
            backtrack = '/..'
            xpath = backtrack + xpath


        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)

    
    def extract_page_url(self, singleSearch: bool = False):
        xpath = '//a'
        attr = '@href'

        if singleSearch:
            backtrack = '/..'
            xpath = backtrack 


        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)
