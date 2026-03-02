import requests
from bs4 import BeautifulSoup
from lxml import etree


class PageFetcher:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

        # t account
        self.proxies = {
            "http": "http://nysekoqg-US-rotate:4ig88f7owcpk@p.webshare.io:80/",
            "https": "http://nysekoqg-US-rotate:4ig88f7owcpk@p.webshare.io:80/",
        }
        # y account
        # self.proxies = {
        #     "http": "http://wdgwqags:e0wk07u371r1@142.111.48.253:7030/",
        #     "https": "http://wdgwqags:e0wk07u371r1@142.111.48.253:7030/",
        # }

    def get_soup(self, pageUrl: str | None = None):
        """
        Use filePath or pageUrl
        Return soup of page
        """
        if pageUrl is not None:
            return self.get_soup_from_url(pageUrl)
        else:
            raise Exception("Please provide Page URL")

    def get_soup_from_url(self, pageUrl):

        try:
            response = requests.get(
                pageUrl, headers=self.headers, proxies=self.proxies, timeout=10
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print("Request failed:", e, flush=True)
            return None

        if response.status_code != 200:
            print(response.status_code)
            print(response.content.decode())
            print("Failed to acces the url")
            return ""
        else:
            soup = BeautifulSoup(response.text, "lxml")

            # Convert BeautifulSoup object to an XPath-compatible structure
            xpathSoup = etree.HTML(str(soup))
            return xpathSoup
