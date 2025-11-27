from scrapers.WebScaper import WebScaper
from scrapers.EpisodeFetcher import EpisodeFetcher
import re

class EpisodeScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def get_episodes(self, number: int = 8):
        """
        Return list numbers of episodes
        """
        episodes = {}
        episodes["Episodes"] = []

        # Get top {number} episodes links
        # Choose option 2 and above, option 1 is junk
        xpath = f'//select[@id="oneclick-episode"]//option[position() > 1 and position() <= {number + 1}]'
        self.soup = self.webScraper.find_all(xpath)

        for index, episodesoup in enumerate(self.soup):
            print(f"Searching for Episode {index + 1}...")


            xpath = ""
            attr = "@value"

            episodePageUrl = self.webScraper.find(xpath=xpath,soup=episodesoup, attr=attr)

            episodePageUrl = episodePageUrl.split("#")[-1]

            episodeFetcher = EpisodeFetcher(pageUrl=episodePageUrl)

            episode = episodeFetcher.get_episode()

            episodes["Episodes"].append(episode)

        return episodes



    def get_episode(self, date: str):
        xpath = f'//select[@id="oneclick-episode"]//option[text()="{date}"]'
        attr = "@value"

        episodePageUrl = self.webScraper.find(xpath=xpath, attr=attr)

        episodePageUrl = episodePageUrl.split("#")[-1]

        episodeFetcher = EpisodeFetcher(pageUrl=episodePageUrl)

        episode = episodeFetcher.get_episode()

        return episode

        
