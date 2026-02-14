from classes.CHANNEL import CHANNEL
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

        channels = []

        for index, channel_soup in enumerate(self.soup):
            print(f"Searching for Channel {index + 1}...", flush=True)
            self.soup = channel_soup

            name = self.extract_name()
            logoUrl = self.extract_icon()
            pageUrl = self.extract_page_url()

            channel = CHANNEL(name=name, logoUrl=logoUrl, pageUrl=pageUrl, id=None)
            channels.append(channel)

        return channels

    def get_channel(self, name: str):
        xpath = f'//h2[text()="{name}"]'
        self.soup = self.webScraper.find(xpath)

        channels = []

        name = self.extract_name(singleSearch=True)
        logoUrl = self.extract_icon(singleSearch=True)
        pageUrl = self.extract_page_url(singleSearch=True)

        channel = CHANNEL(name=name, logoUrl=logoUrl, pageUrl=pageUrl, id=None)

        channels.append(channel)

        return channels

    def extract_name(self, singleSearch: bool = False):
        xpath = "//figure/img"
        attr = "@alt"

        if singleSearch:
            backtrack = "/.."
            xpath = backtrack + xpath

        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)

    def extract_icon(self, singleSearch: bool = False):
        xpath = "//figure/img"
        attr = "@src"

        if singleSearch:
            backtrack = "/.."
            xpath = backtrack + xpath

        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)

    def extract_page_url(self, singleSearch: bool = False):
        xpath = "//a"
        attr = "@href"

        if singleSearch:
            backtrack = "/.."
            xpath = backtrack

        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)
