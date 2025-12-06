from scrapers.WebScaper import WebScaper
from scrapers.EpisodeFetcher import EpisodeFetcher
import re

class EpisodeScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def get_episodes(self, startNumber:int = 1 , endNumber: int = 8):
        """
        Retrieve a json of episode numbers within a specified range.

        Parameters:
        startNumber (int): The starting episode number (inclusive). Defaults to 1.
        endNumber (int): The ending episode number (inclusive). Defaults to 8.

        Returns:
        json: Containing episode data for all episodes 
               in the specified range from startNumber to endNumber.
        """
        if startNumber < 0:
            startNumber = 1
        if endNumber < 0:
            endNumber = 1

        episodes = []

        # Get top {number} episodes links
        # Choose option 2 and above, option 1 is junk
        xpath = f'//select[@id="oneclick-episode"]//option[position() > {startNumber} and position() <= {endNumber}]'
        self.soup = self.webScraper.find_all(xpath)

        for index, episodesoup in enumerate(self.soup):
            print(f"Searching for Episode {index + 1}...")

            xpath = ""
            attr = "@value"

            episodePageUrl = self.webScraper.find(xpath=xpath,soup=episodesoup, attr=attr)

            episodePageUrl = episodePageUrl.split("#")[-1]

            episodeFetcher = EpisodeFetcher(pageUrl=episodePageUrl)

            episode = episodeFetcher.get_episode()

            episodes.append(episode)

        return episodes



    def get_episode(self, date: str):
        xpath = f'//select[@id="oneclick-episode"]//option[text()="{date}"]'
        attr = "@value"

        episodePageUrl = self.webScraper.find(xpath=xpath, attr=attr)

        episodePageUrl = episodePageUrl.split("#")[-1]

        episodeFetcher = EpisodeFetcher(pageUrl=episodePageUrl)

        episode = episodeFetcher.get_episode()

        return episode

        
