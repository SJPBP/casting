from scrapers.PageFetcher import PageFetcher


class WebScaper:
    def __init__(self, pageUrl: str | None = None) -> None:
        self.pageUrl: str | None = pageUrl
        self.pageFetcher = PageFetcher()
        self.soup = ""

    def scrape_page(self):
        """Scrape the page,
        and save it to soup
        and set scraped to true to stop scraping the page again"""
        if not self.scrapedPage:
            self.soup = self.pageFetcher.get_soup(pageUrl=self.pageUrl)
            self.scrapedPage = True
        return self.soup

    def find(self, xpath: str | None, soup=None, attr=None) -> str:
        """Return the text of content found using xpath"""
        if attr is not None:
            xpath = f"{xpath}/{attr}"

        try:
            if soup is None:
                soup = self.scrape_page()
                text: str = soup.xpath(xpath)[0]
            else:
                text: str = soup.xpath(f".{xpath}")[0]
            return text

        except Exception as e:
            print(e)
            exit()

    def find_all(self, xpath: str, soup=None, attr=None) -> str:
        if attr is not None:
            xpath = f"{xpath}/{attr}"

        try:
            if soup is None:
                soup = self.scrape_page()

            url = soup.xpath(xpath)

            return url

        except Exception as e:
            print(e)
            exit()

    def runFunction(self, xpath: str | None, soup=None, attr=None) -> str:
        """Return the result of function found using xpath"""
        if attr is not None:
            xpath = f"{xpath}/{attr}"

        try:
            if soup is None:
                soup = self.scrape_page()  # Get page
                text: str = soup.xpath(xpath)  # Find the data from page
            else:
                text: str = soup.xpath(f".{xpath}")  # Find the data from page
            return text  # Return the data
        except Exception as e:
            print(e)
            exit()
