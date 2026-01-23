from scrapers.WebScaper import WebScaper
from scrapers.EpisodeFetcher import EpisodeFetcher
from classes.EPISODE import EPISODE
from utils.Date import Date
import re

class EpisodeScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)
        self.Date = Date()

    def shallow_search(self, stopDate: str | None = None):
        """
        Retrieve list of all episode date and it's page url 

        And 

        If date given then get episodes data until date excluding date

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

            # Assume site always have newer episode 
            newest_episode_date = self.Date.convert_date_from_apnetv_to_datetime(date)
            
            if stopDate is not None:
                latest_episode_from_db = self.Date.convert_date_from_apnetv_to_datetime(stopDate)

                # There is no new episodes so stop
                if newest_episode_date <= latest_episode_from_db:
                    break

            # Check for newer episodes than from db
            xpath = ""
            attr = "@value"
            episodePageUrl = self.webScraper.find(xpath=xpath,soup=episodesoup, attr=attr)

            episodePageUrl = episodePageUrl.split("#")[-1]

            episode = EPISODE(date=date, pageUrl=episodePageUrl)

            print("Found ", date)
            episodes.append(episode)

        return episodes


    def part_of_above_fun_remove(self):           

            # Find only newer episodes
            if stopDate is not None and newest_episode_date > oldest_episode_date:
                # Find the page url
                xpath = ""
                attr = "@value"
                episodePageUrl = self.webScraper.find(xpath=xpath,soup=episodesoup, attr=attr)

                episodePageUrl = episodePageUrl.split("#")[-1]

                episode = EPISODE(date=date, pageUrl=episodePageUrl)

                print("Adding ", date)
                episodes.append(episode)

            # This means I have reached oldest episode from table
            else:
                # Append newer episodes starting after oldest episode 
                if newest_episode_date != oldest_episode_date and append_episodes > 0:
                    # Find the page url
                    xpath = ""
                    attr = "@value"
                    episodePageUrl = self.webScraper.find(xpath=xpath,soup=episodesoup, attr=attr)

                    episodePageUrl = episodePageUrl.split("#")[-1]

                    episode = EPISODE(date=date, pageUrl=episodePageUrl)

                    print("Adding ", date)
                    episodes.append(episode)

        # Filling episodes from bottom to up
        # reversed = episodes[::-1]
            
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

        
