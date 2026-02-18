import re

from classes.TVSHOW import TVSHOW
from scrapers.WebScaper import WebScaper


class TVShowFetcher:
    def __init__(self, pageUrl: str | None = None, filePath: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl, filePath=filePath)

    def shallow_search(self):
        """
        Retrieve list of all episode date and it's page url

        Returns:
        list: Contains episode data for all episodes but only find date and page url
        """
        # Loop through all the list of episodes on page
        channel = self.extract_channel_name()

        xpath = f'//select[@id="oneclick-episode"]//option[position() > 1 and position() <= 9999999999999]'
        soup = self.webScraper.find_all(xpath)

        episodes = []
        episode = {}

        for index, episodesoup in enumerate(soup):
            # Find the date
            xpath = ""
            attr = "text()"
            date = self.webScraper.find(xpath=xpath, attr=attr, soup=episodesoup)
            episode["date"] = date

            # Find the page url
            xpath = ""
            attr = "@value"
            episodePageUrl = self.webScraper.find(
                xpath=xpath, soup=episodesoup, attr=attr
            )

            episodePageUrl = episodePageUrl.split("#")[-1]
            episode["url"] = episodePageUrl

            episodes.append(episode)

        return episodes

    def get_tv_show(self):
        xpath = "/html/body"
        self.soup = self.webScraper.find(xpath=xpath)

        name = self.extract_name()
        thumbnail = self.extract_icon()
        totalEpisodes = self.extract_total_episodes()
        description = self.extract_description()
        pageUrl = self.extract_page_url()
        channel = self.extract_channel_name()

        # latest_episode = episodeTable.get_all(1, 0)
        # if latest_episode is None:
        #     episodes = scraper.shallow_search
        #     self.update_episodes()

        tvShow = TVSHOW(
            channel=channel,
            name=name,
            thumbnail=thumbnail,
            totalEpisodes=totalEpisodes,
            pageUrl=pageUrl,
            description=description,
        )

        return tvShow

    def extract_page_url(self):
        xpath = '//form[@id="searchform"]'
        attr = "@action"

        self.webScraper.find(xpath=xpath, attr=attr)

    def extract_name(self):
        xpath = '//div[@class="cont-img"]/figure/img'
        attr = "@alt"

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_icon(self):
        xpath = '//div[@class="cont-img"]/figure/img'
        attr = "@src"

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_total_episodes(self):
        xpath = 'count(//select[@id="oneclick-episode"]/option)'

        result = int(self.webScraper.runFunction(xpath=xpath))
        return result

    def extract_channel_name(self):
        xpath = '//h5[@class="contentp-channel-data"]/a'
        attr = "text()"

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_description(self):
        xpath = '//div[@class="story-section"]'
        attr = "text()"

        desc = self.webScraper.find(xpath=xpath, attr=attr).strip()
        return desc
