from concurrent.futures import ThreadPoolExecutor, as_completed

from classes.EPISODE import EPISODE
from scrapers.EpisodeFetcher import EpisodeFetcher
from scrapers.EpisodeScraper import EpisodeScraper
from services.TimerService import TimerService
from tables.Database import Database
from tables.EpisodeTable import EpisodeTable


class EpisodeService:
    def __init__(self, db: Database, tvshowName: str, pageUrl: str):
        """
        Obtain episode data for tvshow

        Parameters:
        db (Database): Connect to database
        tvshowName (str): The title of the TV show for which data is being retrieved.
        pageUrl (str): URL of the TV show page on ApneTV.
        """
        self.db = db
        self.tvshowName = tvshowName
        self.pageUrl = pageUrl

        # get all episodes date and urls and save them in db
        self.shallow_search()

        self.timer = TimerService()

    def shallow_search(self):
        print(f"RUNNING SHALLOW SEARCH ON {self.tvshowName}")
        episodeTable = EpisodeTable(self.db, tvshowName=self.tvshowName)

        episodeScraper = EpisodeScraper(pageUrl=self.pageUrl)

        latest_episode_date: list[EPISODE] | None = episodeTable.latest_episode()

        # Table is filled, but behind then start adding until top episode from table
        if latest_episode_date is None:
            # Find all the episodes
            episodes: list[EPISODE] = episodeScraper.shallow_search()

        else:
            latest_episode_date = latest_episode_date[
                0
            ].convert_date_from_mysql_to_apnetv_format()

            episodes: list[EPISODE] = episodeScraper.shallow_search(latest_episode_date)

        if len(episodes) != 0:
            print("RESUTL FROM SHALLOW SEARCH")
            # Add if there is something inside the list
            episodeTable.batch_insert_all(episodes)

        return True

    def get_episodes(self, startNumber: int, endNumber: int, oldShow: bool = False):
        """
        Retrieve episode data for the selected episode number of the specified TV show.

        Parameters:
        startNumber (int): The starting episode number (inclusive). Defaults to 1.
        endNumber (int): The ending episode number (inclusive). Defaults to 8.
        oldShow (bool): Indicates whether the TV show has concluded; this value is always `False`.
        """
        print(f"GETTING EPISODES FOR TVSHOW: {self.tvshowName}")
        # Connect to db and use table named after tvshow
        episodeTable = EpisodeTable(self.db, tvshowName=self.tvshowName)

        response = {}
        response["Episodes"] = []

        print("GETTING DATA FROM DB")
        # Obtain Episode data from the database.
        episodes: list[EPISODE] = episodeTable.get_all(
            startNumber=startNumber, endNumber=endNumber
        )

        # Prevent putting episodes with completed data
        missing_episode: bool = False

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []

            # Loop through all episode, check if even one episode is missing data then get it
            for idx, episode in enumerate(episodes):
                episode.date = episode.convert_date_from_mysql_to_apnetv_format()
                if episode.contentUrl is None:
                    print(f"MISSING DATA FOR EPISODE WITH DATE: {episode.date}")
                    job = executor.submit(self.process_episode, episode, idx)
                    futures.append(job)

                    missing_episode = True
                else:
                    episodes[idx] = episode
            for future in as_completed(futures):
                updated_episode, idx = future.result()
                episodes[idx] = updated_episode

        # I have some episode(s) that are missing data
        if missing_episode:
            print("SAVING EPISODES DATA TO DB")
            # Add if there is something inside the list
            episodeTable.batch_update_all(episodes)

        response["Episodes"].append(episodes)

        return response

    def process_episode(self, episode, idx):
        # There is no extra episode details in db
        scraper = EpisodeFetcher(episode.pageUrl)

        result = scraper.get_episode()

        return result, idx

    def get_episode(self, date: str) -> dict:
        """
        Retrieve episode data for a specific date of the given TV show.

        Parameters:
        date (str): The date for which to retrieve episode data.
        """
        table = EpisodeTable(self.db, tvshowName=self.tvshowName)

        response = {}
        response["Episodes"] = []

        # Obtain Episode data from the database.
        episode = table.get_by_date(date)
        print(episode)

        # Episode data is not in the database.
        # So it means there is no episode fot that date
        if episode is None:
            return response

        if episode.contentUrl is None:
            print("Finding all episode data")
            scraper = EpisodeFetcher(episode.pageUrl)

            episode = scraper.get_episode()
            print("Done")

            table.update(episode)
        else:
            episode.date = episode.convert_date_from_mysql_to_apnetv_format()

        response["Episodes"].append(episode)

        return response
