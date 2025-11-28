from scrapers.EpisodeScraper import EpisodeScraper
from tables.EpisodeTable import EpisodeTable
from tables.Database import Database

class EpisodeService:
    def __init__(self, db: Database, tvshow: str):
        self.db = db
        self.tvshow = tvshow
        self.table = EpisodeTable(self.db, tvshowName=tvshow)

    def get_episodes(self, pageUrl: str, numberOfEpisodes: int, oldShow: bool = False):
        response = {}
        response["Episodes"] = []

        episodes = self.table.get_all()

        if episodes is None:
            scraper = EpisodeScraper(pageUrl)
            episodes = scraper.get_episodes(numberOfEpisodes)
            episodes = self.table.insert_all(episodes)

        for episode in episodes:
            episode.date = episode.convert_date_to_apnetv_format()
            response["Episodes"].append(episode.json)

        return response

    def get_episode(self, pageUrl: str, date: str):
        response = {}
        response["Episodes"] = []

        episode = self.table.get_by_date(date)

        if episode is None:
            return None
            scraper = episodeScraper(self.pageUrl)
            episode = scraper.get_episode(name)
            self.table.insert(episode["episodes"][0])

        episode.date = episode.convert_date_to_apnetv_format()

        response["Episodes"].append(episode.json)

        return response

