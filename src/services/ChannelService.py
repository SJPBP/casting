from scrapers.ChannelScraper import ChannelScraper
from tables.ChannelTable import ChannelTable
from classes.CHANNEL import CHANNEL
from tables.Database import Database

class ChannelService:
    def __init__(self, db: Database):
        """
        Intizale Channel Service.

        Parameters:
        db (Database): Allows to work with database
        """
        self.db = db
        self.table = ChannelTable(self.db)

        # This ApneTV Main Page
        # This is the base or start page for scraping
        self.pageUrl = "https://apnetv.xyz/"

    def get_channels(self):
        """
        Obtain data of all the channels on ApneTV

        Parameters:
        None

        Return:
        json: Data of channels
        """

        response = {}
        response["Channels"] = []

        # Obtain data of channels stored in database
        channels = self.table.get_all()

        # There is no data on channels in db
        if channels is None:
            # Obtain the data from the website
            scraper = ChannelScraper(self.pageUrl)
            channels = scraper.get_channels()
            channels = self.table.insert_all(channels)

        # Put the data for each channel in json
        for chn in channels:
            response["Channels"].append(chn.json)

        return response

    def get_channel(self, name: str) -> dict:
        """
        Obtain data of channel choosen on ApneTV

        Parameters:
        Name (str): Name of channel on ApneTV 

        Return:
        json: Data of channel
        """
        response = {}
        response["Channels"] = []

        # Obtain data of channel stored in database
        channel = self.table.get_by_name(name)

        # There is no data on channel in db
        if channel is None:
            # Obtain the data from the website
            scraper = ChannelScraper(self.pageUrl)
            channel = scraper.get_channel(name)
            self.table.insert(channel["Channels"][0])

        # Put the data of channel in json
        response["Channels"].append(channel.json)

        return response




