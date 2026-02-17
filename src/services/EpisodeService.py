from classes.EPISODE import EPISODE
from scrapers import EpisodeFetcher
from scrapers.EpisodeFetcher import EpisodeFetcher
from scrapers.EpisodeScraper import EpisodeScraper
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
        self.shallow_search()

    def shallow_search(self):
        episodeTable = EpisodeTable(self.db, tvshowName=self.tvshowName)

        episodeScraper = EpisodeScraper(pageUrl=self.pageUrl)

        latest_episode_date: list[EPISODE] = episodeTable.latest_episode()

        # Table is filled, but behind then start adding until top episode from table
        if latest_episode_date is not None:
            latest_episode_date = latest_episode_date[
                0
            ].convert_date_from_mysql_to_apnetv_format()

            print("Latest_Episode", latest_episode_date)
            episodes: list[EPISODE] = episodeScraper.shallow_search(latest_episode_date)

        else:
            # Find all the episodes
            episodes: list[EPISODE] = episodeScraper.shallow_search()
        if episodes:
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
        # Connect to db and use table named after tvshow
        episodeTable = EpisodeTable(self.db, tvshowName=self.tvshowName)

        response = {}
        response["Episodes"] = []

        # Obtain Episode data from the database.
        episodes = episodeTable.get_all(startNumber=startNumber, endNumber=endNumber)

        if episodes is not None:
            # Get the episode data for the one that don't have all the data
            for index, episode in enumerate(episodes):
                if episode.contentUrl is None:
                    print("Finding ")
                    scraper = EpisodeFetcher(episode.pageUrl)

                    result = scraper.get_episode()

                    episodeTable.update(result)

                    episodes[index] = result

                episode.date = episode.convert_date_from_mysql_to_apnetv_format()

            if episodes:
                # Add if there is something inside the list
                episodeTable.batch_insert_all(episodes)

            response["Episodes"].append(episodes)

        return response

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
