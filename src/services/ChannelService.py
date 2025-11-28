from scrapers.ChannelScraper import ChannelScraper
from tables.ChannelTable import ChannelTable
from classes.CHANNEL import CHANNEL
from tables.Database import Database

class ChannelService:
    def __init__(self, db: Database):
        self.db = db
        self.table = ChannelTable(self.db)

        # This ApneTV Main Page
        self.pageUrl = "https://apnetv.xyz/"

    def get_channels(self):
        response = {}
        response["Channels"] = []

        channels = self.table.get_all()

        if channels is None:
            scraper = ChannelScraper(self.pageUrl)
            channels = scraper.get_channels()
            channels = self.table.insert_all(channels)

        for chn in channels:
            response["Channels"].append(chn.json)

        return response

    def get_channel(self, name: str):
        response = {}
        response["Channels"] = []

        channel = self.table.get_by_name(name)

        if channel is None:
            return None
            scraper = ChannelScraper(self.pageUrl)
            channel = scraper.get_channel(name)
            self.table.insert(channel["Channels"][0])

        response["Channels"].append(channel.json)

        return response




