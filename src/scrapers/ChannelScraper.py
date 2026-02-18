from asyncio import futures
from concurrent.futures import ThreadPoolExecutor, as_completed

from classes.CHANNEL import CHANNEL
from scrapers.WebScaper import WebScaper
from services.TimerService import TimerService


class ChannelScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)
        self.timer = TimerService()

    def get_channels(self):
        """
        Return list of channels
        """
        self.timer.start_timer("find_channels")
        xpath = '//div[@class="channel-title-logo"]'
        soups = self.webScraper.find_all(xpath)

        channels = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for index, channel_soup in enumerate(soups):
                print(f"Searching for Channel {index + 1}...", flush=True)
                soup = channel_soup

                # Get site in background
                job = executor.submit(
                    self.extract_data, soup=soup, allowSingleSearch=False
                )
                futures.append(job)

            # Add results that are done in channels
            for future in as_completed(futures):
                channels.append(future.result())

        total_time = self.timer.end_timer("find_channels")

        print(
            f"Finished extracting data about all channels using thread in {total_time:.2f} seconds"
        )

        return channels

    def get_channel(self, name: str):
        self.timer.start_timer("find_channel")

        xpath = f'//h2[text()="{name}"]'

        soup = self.webScraper.find(xpath)

        channels = []
        channel = self.extract_data(soup=soup, allowSingleSearch=True)

        channels.append(channel)

        total_time = self.timer.end_timer("find_channel")
        print(
            f"Finished extracting data about channel {name} in {total_time:.2f} seconds"
        )

        return channels

    def extract_data(self, soup, allowSingleSearch=False):
        self.timer.start_timer("EX")

        name = self.extract_name(soup=soup, singleSearch=allowSingleSearch)
        logoUrl = self.extract_icon(soup=soup, singleSearch=allowSingleSearch)
        pageUrl = self.extract_page_url(soup=soup, singleSearch=allowSingleSearch)

        channel = CHANNEL(name=name, logoUrl=logoUrl, pageUrl=pageUrl, id=None)

        total_time = self.timer.end_timer("EX")
        print(
            f"Finished extracting all data from the soup in {total_time:.1f} seconds."
        )

        return channel

    def extract_name(self, soup, singleSearch: bool):
        xpath = "//figure/img"
        attr = "@alt"

        if singleSearch:
            backtrack = "/.."
            xpath = backtrack + xpath

        # find channel name
        return self.webScraper.find(xpath=xpath, soup=soup, attr=attr)

    def extract_icon(self, soup, singleSearch: bool):
        xpath = "//figure/img"
        attr = "@src"

        if singleSearch:
            backtrack = "/.."
            xpath = backtrack + xpath

        # find channel icon
        return self.webScraper.find(xpath=xpath, soup=soup, attr=attr)

    def extract_page_url(self, soup, singleSearch: bool):
        xpath = "//a"
        attr = "@href"

        if singleSearch:
            backtrack = "/.."
            xpath = backtrack

        # find channel page url
        return self.webScraper.find(xpath=xpath, soup=soup, attr=attr)
