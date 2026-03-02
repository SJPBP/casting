from concurrent.futures import ThreadPoolExecutor, as_completed

from classes.EPISODE import EPISODE
from scrapers.EpisodeFetcher import EpisodeFetcher
from scrapers.WebScaper import WebScaper
from services.TimerService import TimerService
from utils.Date import Date


class EpisodeScraper:
    def __init__(self, pageUrl: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl)
        self.timer = TimerService()
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
        total = 0

        for index, episodesoup in enumerate(soup):
            self.timer.start_timer("shallow")
            # Find the date
            xpath = ""
            attr = "text()"
            date = self.webScraper.find(xpath=xpath, attr=attr, soup=episodesoup)

            # Assume site always have newer episode
            newest_episode_date = self.Date.convert_date_from_apnetv_to_datetime(date)

            if stopDate is not None:
                # StopDate is date of latest episode saved in db
                latest_episode_from_db = self.Date.convert_date_from_apnetv_to_datetime(
                    stopDate
                )

                # There is no new episodes on website than one from db so stop
                if newest_episode_date <= latest_episode_from_db:
                    break

            # Check for newer episodes than from db
            xpath = ""
            attr = "@value"
            episodePageUrl = self.webScraper.find(
                xpath=xpath, soup=episodesoup, attr=attr
            )

            episodePageUrl = episodePageUrl.split("#")[-1]

            episode = EPISODE(date=date, pageUrl=episodePageUrl)

            # print("Found ", date)
            total += self.timer.end_timer("shallow")
            episodes.append(episode)

        print(f"Shallow Search Time: {total}")
        return episodes

    def get_episodes(self, startNumber: int = 1, endNumber: int = 8):
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

        futures = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            # Get top {number} episodes links
            # Choose option 2 and above, option 1 is junk
            xpath = f'//select[@id="oneclick-episode"]//option[position() > {startNumber} and position() <= {endNumber}]'
            self.soup = self.webScraper.find_all(xpath)

            for index, episodesoup in enumerate(self.soup):
                print(f"Searching for Episode {index + 1}...")

                # Finding tvshow in background
                job = executor.submit(self.extract_data, soup=episodesoup)
                futures.append(job)

        for future in as_completed(futures):
            episodes.append(future.result())

        total_time = self.timer.end_timer("EX")
        print(
            f"Finished extracting all data from the soup in {total_time:.1f} seconds."
        )
        return episodes

    def extract_data(self, soup):
        xpath = ""
        attr = "@value"

        episodePageUrl = self.webScraper.find(xpath=xpath, soup=soup, attr=attr)

        episodePageUrl = episodePageUrl.split("#")[-1]

        episodeFetcher = EpisodeFetcher(pageUrl=episodePageUrl)

        episode = episodeFetcher.get_episode()

        return episode
