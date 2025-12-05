from scrapers.EpisodeScraper import EpisodeScraper
from tables.EpisodeTable import EpisodeTable
from tables.Database import Database

class EpisodeService:
    def __init__(self, db: Database):
        """
        Obtain episode data for tvshow

        Parameters:
        db (Database): Connect to database
        """
        self.db = db
        

    def get_episodes(self, tvshow: str, pageUrl: str, numberOfEpisodes: int, oldShow: bool = False):
        """
        Retrieve episode data for the selected episode number of the specified TV show.

        Parameters:
        pageUrl (str): URL of the TV show page on ApneTV.
        numberOfEpisodes (int): The total number of episodes for which to retrieve data.
        oldShow (bool): Indicates whether the TV show has concluded; this value is always `False`. 
        tvshow (str): The title of the TV show for which data is being retrieved.
        """
        # Connect to db and use table named after tvshow 
        table = EpisodeTable(self.db, tvshowName=tvshow)

        response = {}
        response["Episodes"] = []

        # Obtain Episode data from the database.
        episodes = table.get_all()

        # Episode data is not in the database.
        if episodes is None:
            # Obtain the data from the website
            scraper = EpisodeScraper(pageUrl)
            episodes = scraper.get_episodes(numberOfEpisodes)
            episodes = table.insert_all(episodes)

        for episode in episodes:
            episode.date = episode.convert_date_to_apnetv_format()
            response["Episodes"].append(episode.json)

        return response

    def get_episode(self, tvshow: str, pageUrl: str, date: str):
        """
        Retrieve episode data for a specific date of the given TV show.

        Parameters:
        tvshow (str): The title of the TV show for which data is being retrieved.
        pageUrl (str): URL of the TV show page on ApneTV.
        date (str): The date for which to retrieve episode data.
        """
        table = EpisodeTable(self.db, tvshowName=tvshow)

        response = {}
        response["Episodes"] = []

        # Obtain Episode data from the database.
        episode = table.get_by_date(date)

        # Episode data is not in the database.
        if episode is None:
            # Obtain the data from the website
            scraper = episodeScraper(self.pageUrl)
            episode = scraper.get_episode(name)
            table.insert(episode["episodes"][0])

        episode.date = episode.convert_date_to_apnetv_format()

        response["Episodes"].append(episode.json)

        return response

