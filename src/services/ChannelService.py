from concurrent.futures import ThreadPoolExecutor

from scrapers.ChannelScraper import ChannelScraper
from tables.ChannelTable import ChannelTable
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

        self.executor = ThreadPoolExecutor(max_workers=5)

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

            # Run DB save in background
            self.executor.submit(self.save_to_db, self.db, channels)

            # channels = self.table.insert_all(channels)

        # Put the data for each channel in json
        for chn in channels:
            response["Channels"].append(chn)

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
        channel = None

        # There is no data on channel in db
        if channel is None:
            # Obtain the data from the website
            scraper = ChannelScraper(self.pageUrl)
            channel = scraper.get_channel(name)
            self.table.insert(channel[0])

        # Put the data of channel in json
        response["Channels"].append(channel)

        return response

    def save_to_db(self, db, channels):
        # Connect to table that will save data
        table = ChannelTable(db)

        # Now save it
        table.insert_all(channels)
