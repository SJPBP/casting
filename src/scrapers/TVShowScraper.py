from scrapers.WebScaper import WebScaper
from scrapers.TVShowFetcher import TVShowFetcher
import re

class TVShowScraper:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def get_tv_shows(self):
        """
        Return list of tv shows
        """
        tvShows = {}
        tvShows["TvShows"] = []

        # Looking for current tv shows
        xpath = '//li[@class="serial-item"]'
        self.soup = self.webScraper.find_all(xpath)

        for index, tvShowSoup in enumerate(self.soup):
            print(f"Searching for Currently Running TV Show {index}...")

            self.soup = tvShowSoup

            tvShows = {}
            tvShows["TvShows"] = []

            pageUrl = self.extract_new_page_url()

            tvShowFetcher = TVShowFetcher(pageUrl=pageUrl)
            tvShow = tvShowFetcher.get_tv_show()

            tvShows["TvShows"].append(tvShow)

        # Looking for old tv shows
        xpath = '//ul[@class="old-link-list"]/li'
        self.soup = self.webScraper.find_all(xpath)

        for index, tvShowSoup in enumerate(self.soup):
            print(f"Searching for Old TV Show {index}...")

            self.soup = tvShowSoup
            tvShow = {}
            tvShow["TvShow"] = {}
            
            pageUrl = self.extract_old_page_url()

            tvShowFetcher = TVShowFetcher(pageUrl=pageUrl)
            tvShow = tvShowFetcher.get_tv_show()

            tvShows["TvShows"].append(tvShow)

        return tvShows


    def get_tv_show(self, name: str):
        newTvShowXpath = f'//div[@data-name="{name}"]'
        
        try:
            print("Finding new TV")
            self.soup = self.webScraper.find(newTvShowXpath)

            pageUrl = self.extract_new_page_url()
            print("DONE")
        except Exception:
            pageUrl = None # Making sure there is no problem for next operations
            print("Could't find in currently running tv shows")

        if pageUrl is None:
            oldTvShowXpath = f'//ul[@class="old-link-list"]/li/a[@title="{name}"]'

            self.soup = self.webScraper.find(oldTvShowXpath)

            pageUrl = self.extract_old_page_url(singleSearch=True)

        tvShowFetcher = TVShowFetcher(pageUrl=pageUrl)

        tvShow = tvShowFetcher.get_tv_show()

        return tvShow

    
    def extract_new_page_url(self, singleSearch: bool = False):
        xpath = '/a'
        attr = '@href'

        if singleSearch:
            xpath = "/.." + xpath

        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)

    def extract_old_page_url(self, singleSearch: bool = False):
        xpath = '/a'
        attr = '@href'

        if singleSearch:
            xpath = "/.." + xpath

        return self.webScraper.find(xpath=xpath, soup=self.soup, attr=attr)
