from scrapers.TVShowScraper import TVShowScraper
from tables.TvShowTable import TvShowTable
from classes.TVSHOW import TVSHOW
from tables.Database import Database

class TVShowService:
    def __init__(self, db: Database, channel: str):
        self.db = db
        self.channel = channel
        self.table = TvShowTable(self.db, channel=channel)

    def get_tvshows(self, pageUrl: str):
        response = {}
        response["TVShows"] = []

        tvshows = self.table.get_all(self.channel)

        if tvshows is None:
            scraper = TVShowScraper(pageUrl)
            tvshows = scraper.get_tv_shows()
            tvshows = self.table.insert_all(tvshows)

        for tvshow in tvshows:
            response["TVShows"].append(tvshow.json)

        return response

    def get_tvshow(self, pageUrl: str, name: str):
        response = {}
        response["TVShows"] = []

        tvshow = self.table.get_by_channel(name)

        if tvshow is None:
            return None
            scraper = TVShowScraper(self.pageUrl)
            tvshow = scraper.get_tvshow(name)
            self.table.insert(tvshow["TVShows"][0])

        response["TVShows"].append(tvshow.json)

        return response

