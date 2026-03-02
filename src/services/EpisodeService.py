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

        self.timer = TimerService()

        self.episode_time = 0

        # Needs to be global to make thread work in background
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.tries = 3  # After this is 0 run shallow_search in get_episodes

        # get all episodes date and urls and save them in db
        self.shallow_search()

        self.timer = TimerService()

    def shallow_search(self):
        print(f"Running Shallow Search On TV Show: {self.tvshowName}")
        episodeTable = EpisodeTable(self.db, tvshowName=self.tvshowName)

        # Scrape the page with episode date and url
        episodeScraper = EpisodeScraper(pageUrl=self.pageUrl)

        # Check if there is episode and get it
        latest_episode_date: list[EPISODE] | None = episodeTable.latest_episode()

        # There is no episode data saved to db
        if latest_episode_date is not None:
            # Get all the episodes from the scraped page
            print("Getting Every Episodes Data")
            episodes: list[EPISODE] = episodeScraper.shallow_search()

        else:
            # Convert the episode date to one used in ApneTV
            latest_episode_date = latest_episode_date[
                0
            ].convert_date_from_mysql_to_apnetv_format()

            print(f"Getting Episodes Uploaded After: {latest_episode_date}")

            # Get all the episodes released after latest episode saved in db
            episodes: list[EPISODE] = episodeScraper.shallow_search(latest_episode_date)

        print("Saving Episode Data")

        # Save data to db in background
        # self.executor.submit(self.insert_all_to_db, self.db, self.tvshowName, episodes)

        # Save it for later use
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

        print(f"TRIES LEFT: {self.tries}")
        run = False
        if self.tries == 0:
            run = True

            # self.shallow_search()
        else:
            self.tries = 0
        print(f"TRIES LEFT: {self.tries}")
        print(f"Runned: {run}")

        response = {}
        response["Episodes"] = []

        print("GETTING DATA FROM DB")

        self.timer.start_timer("g")
        # Connect to db and use table named after tvshow
        episodeTable = EpisodeTable(self.db, tvshowName=self.tvshowName)

        # Obtain Episode data from the database.
        episodes: list[EPISODE] = episodeTable.get_all(
            startNumber=startNumber, endNumber=endNumber
        )
        total = self.timer.end_timer("g")
        print(f"Getting Data from DB Time: {total}")

        # Couldn't connect to database
        # So I can't run next code so just stop
        if episodes is False:
            return response

        # Prevent putting episodes with completed data in db
        # Means there is data which missing in db so I have to things I need to save
        missing_episode: bool = False

        self.timer.start_timer("p")
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = []

            # Loop through all episode, check if even one episode is missing data then get it
            for idx, episode in enumerate(episodes):
                episode.date = episode.convert_date_from_mysql_to_apnetv_format()

                if episode.contentUrl is None:
                    # There is missing episode so I will have to run method to save to db
                    missing_episode = True

                    print(f"MISSING DATA FOR EPISODE WITH DATE: {episode.date}")

                    # Get episode data in background
                    job = executor.submit(self.process_episode, episode, idx)
                    futures.append(job)

                # TODO: Check If This Commenting Else Statement Cause Error
                # If Yes Remove comment else Remove Else Statement
                # else:
                #     # Data is not missing so add to
                #     episodes[idx] = episode

            for future in as_completed(futures):
                # Get Missing data obtained from website
                updated_episode, idx = future.result()

                # Save the data from where it takes from in list
                episodes[idx] = updated_episode

        # I have some episode(s) that are missing data
        if missing_episode:
            # self.db_executor.submit(self.save_to_db, self.db, self.tvshowName, episodes)

            # Run DB save in background
            self.executor.submit(
                self.update_all_to_db, self.db, self.tvshowName, episodes
            )

            # episodeTable.batch_update_all(episodes)

        response["Episodes"].append(episodes)
        self.episode_time = self.timer.end_timer("p")
        print(f"TOOK Time to process data: {self.episode_time}")

        print("RETURNING DATA")

        return response

    def insert_all_to_db(self, db, tvshowName, episodes):
        # Connect to table that will save data
        episodeTable = EpisodeTable(db, tvshowName=tvshowName)

        # Now save it
        episodeTable.batch_insert_all(episodes)

    def update_all_to_db(self, db, tvshowName, episodes):
        print("SAVING EPISODES DATA TO DB")

        # Connect to table that will save data
        episodeTable = EpisodeTable(db, tvshowName=tvshowName)

        # Now save it
        episodeTable.batch_update_all(episodes)

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
