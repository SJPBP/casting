from concurrent.futures import ThreadPoolExecutor, as_completed

from scrapers.TVShowFetcher import TVShowFetcher
from scrapers.WebScaper import WebScaper
from services.TimerService import TimerService


class TVShowScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)
        self.timer = TimerService()

    def get_tv_shows(self):
        """
        Return list of tv shows
        """
        self.timer.start_timer("EX")

        tvShows = []

        futures = []

        with ThreadPoolExecutor(max_workers=9) as executor:
            # Looking for current tv shows
            xpath = '//li[@class="serial-item"]'
            self.soup = self.webScraper.find_all(xpath)
            for index, tvShowSoup in enumerate(self.soup):
                print(f"Searching for Currently Running TV Show {index}...")

                soup = tvShowSoup

                # Finding tvshow in background
                job = executor.submit(
                    self.extract_tvshows_data, soup=soup, finding_old_show=False
                )
                futures.append(job)

        with ThreadPoolExecutor(max_workers=9) as executor:
            # Looking for old tv shows
            xpath = '//ul[@class="old-link-list"]/li'
            self.soup = self.webScraper.find_all(xpath)

            for index, tvShowSoup in enumerate(self.soup):
                print(f"Searching for Old TV Show {index}...")

                soup = tvShowSoup

                # Finding tvshow in background
                job = executor.submit(
                    self.extract_tvshows_data, soup=soup, finding_old_show=True
                )
                futures.append(job)

        for future in as_completed(futures):
            tvShows.append(future.result())

        total_time = self.timer.end_timer("EX")
        print(
            f"Finished extracting all data from the soup in {total_time:.1f} seconds."
        )
        return tvShows

    def extract_tvshows_data(self, soup, finding_old_show: bool = False):
        self.timer.start_timer("EX")

        # Different type of show needed different type of xpath
        if finding_old_show:
            pageUrl = self.extract_old_page_url(soup=soup)
        else:
            pageUrl = self.extract_new_page_url(soup=soup)

        tvShowFetcher = TVShowFetcher(pageUrl=pageUrl)

        tvShow = tvShowFetcher.get_tv_show()

        tvShow.pageUrl = pageUrl

        total_time = self.timer.end_timer("EX")
        print(
            f"Finished extracting all data from the soup in {total_time:.1f} seconds."
        )

        return tvShow

    def extract_new_page_url(self, soup):
        xpath = "/a"
        attr = "@href"

        return self.webScraper.find(xpath=xpath, soup=soup, attr=attr)

    def extract_old_page_url(self, soup):
        xpath = "/a"
        attr = "@href"

        return self.webScraper.find(xpath=xpath, soup=soup, attr=attr)
