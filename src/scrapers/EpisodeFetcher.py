import re

from classes.EPISODE import EPISODE
from scrapers.WebScaper import WebScaper


class EpisodeFetcher:
    def __init__(self, pageUrl: str | None = None) -> None:
        self.webScraper = WebScaper(pageUrl=pageUrl)
        self.pageUrl = pageUrl

    def get_episode(self):
        date: str = str(self.extract_date())
        title: str = str(self.extract_title())
        thumbnail: str = str(self.extract_thumbnail())
        contentUrl: str = str(self.extract_content_url())

        episode = EPISODE(
            date=date,
            pageUrl=self.pageUrl,
            thumbnail=thumbnail,
            contentUrl=contentUrl,
            title=title,
        )

        episode.contentType = episode.update_content_type()

        return episode

    def extract_date(self):
        xpath = '//li[@class="active"]'
        attr = "text()"

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_title(self):
        xpath = '//h4[@class="subheading"]'
        attr = "text()"

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_thumbnail(self):
        xpath = '//figure[@class="episodethumb"]/img'
        attr = "@src"

        return self.webScraper.find(xpath=xpath, attr=attr)

    def extract_content_url(self):
        xpath = '//div[@id="video_player"]//following-sibling::script[@type="text/javascript"]'
        attr = "text()"

        source = self.webScraper.find(xpath=xpath, attr=attr)

        pattern = r"\"(https?://[^\"]+)\""
        url = (re.search(pattern, source)).group(1)

        return url
