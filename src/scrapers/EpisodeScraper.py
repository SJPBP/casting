from scrapers.WebScaper import WebScaper
from scrapers.EpisodeFetcher import EpisodeFetcher
from classes.EPISODE import EPISODE
import re

class EpisodeScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def shallow_search(self):
        """
        Retrieve list of all episode date and it's page url

        Returns:
        list: Contains episode data for all episodes but only find date and page url
        """
        # Loop through all the list of episodes on page
        xpath = f'//select[@id="oneclick-episode"]//option[position() > 1 and position() <= 9999999999999]'
        soup = self.webScraper.find_all(xpath)

        episodes = []
        for index, episodesoup in enumerate(soup):
            # Find the date
            xpath = ""
            attr = "text()"
            date = self.webScraper.find(xpath=xpath, attr=attr, soup=episodesoup)

            # Find the page url
            xpath = ""
            attr = "@value"
            episodePageUrl = self.webScraper.find(xpath=xpath,soup=episodesoup, attr=attr)

            episodePageUrl = episodePageUrl.split("#")[-1]

            episode = EPISODE(date=date, pageUrl=episodePageUrl)

            episodes.append(episode)
            
        return episodes


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

            episodePageUrl = self.webScraper.find(xpath=xpath, soup=episodesoup, attr=attr)

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

        
