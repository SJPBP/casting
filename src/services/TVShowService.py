from concurrent.futures import ThreadPoolExecutor

from classes.TVSHOW import TVSHOW
from scrapers.TVShowScraper import TVShowScraper
from tables.Database import Database
from tables.TvShowTable import TvShowTable


class TVShowService:
    def __init__(self, db: Database):
        """
        Obtain tv show data for channel

        Parameters:
        db (Database): Connect to database
        """
        self.db = db

        # Needs to be global to make thread work in background
        self.executor = ThreadPoolExecutor(max_workers=5)

    def get_tvshows(self, channel: str, pageUrl: str):
        """
                Retrieve data for the TV shows in given channel.

                Parameters:
                channel (str): The title of the channel for which data is being retrieved.
        pageUrl (str): URL of the channel page on ApneTV.
        """
        # Connect to db and use table named after channel
        table = TvShowTable(self.db, channel=channel)

        response = {}
        response["TVShows"] = []

        # Obtain TV Show data from the database.
        tvshows = table.get_all(channel)

        # TV show data is not in the database.
        if tvshows is None:
            # Obtain the data from the website
            scraper = TVShowScraper(pageUrl)
            tvshows = scraper.get_tv_shows()

            # Run DB save in background
            self.executor.submit(self.save_to_db, self.db, channel, tvshows)

        for tvshow in tvshows:
            response["TVShows"].append(tvshow)

        return response

    def get_tvshow(self, channel: str, pageUrl: str, name: str):
        """
        Retrieve data for the specified TV show in given channel.

        Parameters:
        channel (str): The title of the channel for which data is being retrieved.
        pageUrl (str): URL of the channel page on ApneTV.
        name (str): The title of the TV show for which data is being retrieved.
        """
        table = TvShowTable(self.db, channel=channel)
        show = TVSHOW(channel=channel, pageUrl=pageUrl, name=name)

        response = {}
        response["TVShows"] = []

        # TV show data is not in the database.
        tvshow = table.get_by_channel(show)

        # None: There is no data on tv show in db
        # False: Couldn't even connect to db
        if tvshow is None or tvshow is False:
            # Obtain the data from the website
            scraper = TVShowScraper(pageUrl)

            tvshow = scraper.get_tvshow(name)

            # Save data to db
            table.insert(tvshow["TVShows"][0])

        response["TVShows"].append(tvshow)

        return response

    def save_to_db(self, db, channel, tvshows):
        # Connect to table that will save data
        table = TvShowTable(db, channel=channel)

        # Now save it
        table.insert_all(tvshows)
