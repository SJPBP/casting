from classes import EPISODE
from scrapers.TVShowScraper import TVShowScraper
from tables.TvShowTable import TvShowTable
from tables.EpisodeTable import EpisodeTable
from classes.TVSHOW import TVSHOW
from tables.Database import Database

class TVShowService:
    def __init__(self, db: Database):
        """
        Obtain tv show data for channel

        Parameters:
        db (Database): Connect to database
        """
        self.db = db
    
    def update_episodes(self, tvshowName: str, episodes):
        """I will add the data to episode table"""
        episodeTable = EpisodeTable(self.db, tvshowName)
        episodeTable.insert_all(episodes)
    

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
            tvshows = table.insert_all(tvshows)

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

        if tvshow is None:
            # Obtain the data from the website
            scraper = TVShowScraper(pageUrl)
            tvshow = scraper.get_tvshow(name)
            table.insert(tvshow["TVShows"][0])

        episodeTable = EpisodeTable(self.db, tvshow.name)

        

        response["TVShows"].append(tvshow)

        return response

