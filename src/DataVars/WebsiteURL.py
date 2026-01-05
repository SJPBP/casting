import requests
from datetime import date


class WebsiteURL:
    def __init__(self, websiteURL=None):
        self.websiteURL: str = websiteURL  # TODO: Use vaildation function
        self.htmlData: str = None

    def getWebsiteSourceFromOnline(self) -> None:
        '''Go to website and get the html data and store it in htmlData'''
        if self.websiteURL != None:
            # Get the html file of website
            response: str = requests.get(self.websiteURL)

            # TODO: Use switch function to handle different status codes
            # Check if html file was obtained
            if response.status_code == 200:
                self.htmlData = response.text
            else:
                print(f"Failed to retrieve data {response.status_code}")
        else:
            print("Please give the website url")

    # TODO: Add a vaildation function for the websiteURL which going used in __init__



