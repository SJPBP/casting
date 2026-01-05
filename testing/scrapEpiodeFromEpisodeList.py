# import requests
from bs4 import BeautifulSoup
from datetime import date
import pychromecast
import requests
import re
import time


class Episode:
    def __init__(self):
        pass

    def getLatestEpisode(self) -> str:

        # with open("./updatedTmkocEpisodesLists.html") as episodeFile:
        websiteURL = "https://apnetv.biz/Hindi-Serial/Taarak-Mehta-Ka-Ooltah-Chashmah"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(websiteURL, headers=headers)

        if response.status_code != 200:
            print(response.status_code)
            print(response.content.decode())
            print("Failed to acces the url")

        else:
            soup = BeautifulSoup(response.text, 'lxml')

            # print(soup.prettify())
            # episodes = soup.find_all("div", class_="shows-box")

            # Gets tmkoc latest episode html data
            episode = soup.find("div", class_="shows-box")

            # videoOptionLists = episodes.find("span", class_="episode-name").text

            # Get Today date in DDth M YYYY
            today = date.today()
            todayDate = today.strftime("%dth %B %Y")

            #
            episodeVideoUrlsPage = episode.find("a")["href"]
            episodeDate = episode.find("span", class_="episode-name").text

            if str(todayDate) == str(episodeDate):
                print("Today Episode is Avaiable")
                print(episodeVideoUrlsPage)
                return episodeVideoUrlsPage

            else:
                print(f"Latest Episode is of {episodeDate}")
                print("Today Episode is not Avaiable right now, Please wait")

    def getEpisodePremiumVideoLink(self, websiteURL: str) -> str:
        print("Getting Premium Video Website Url")
        print(websiteURL)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(websiteURL, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            # Source: https://stackoverflow.com/a/26192778
            videoLink = soup.find("div", id="playerwrap").find(
                "script", type="text/javascript")

            # Extract Premium link of episode
            pattern = r'\"(https?://[^\"]+)\"'
            match = re.search(pattern, videoLink.text)

            # Check if a match is found and extract the token
            if match:
                token = match.group(1)  # Extract the token value
                print("Premium video link found.")  # Print the token
                return token
            else:
                print("Premium video link not found.")

        else:
            print(f"Failed to get Data {response}")

    def castEpisodePremiumVideoLink(self, premiumVideoLink: str, chromeCastDeviceName: list = ["Living Room TV"]) -> None:
        '''Cast premium video link from given website url'''

        # chromecast, browser = pychromecast.get_listed_chromecasts(
        #     ["Living Room TV", "Sofa Room TV"])

        chromecast, browser = pychromecast.get_listed_chromecasts(
            chromeCastDeviceName)

        livingRoomTV = chromecast[0]
        print("Found Living Room TV")

        # MEDIA_URL = "https://si.videoapne.to/hls/,bdohxn4p7bboxuzvta474gkxtfyg5xmxxuv6gu7mu46gqsrkennd2qvdyfgq,.urlset/master.m3u8"
        # LocalURL = ""
        # print(chromecast)

        # Start socket client's worker thread and wait for initial status update
        livingRoomTV.wait()

        livingRoomTV.quit_app()
        # Send media to this object to cast to TV
        livingRoomMediaController = livingRoomTV.media_controller

        livingRoomMediaController.play_media(
            premiumVideoLink, "video/mp4")

        livingRoomMediaController.block_until_active()

        player_state = None
        t = 30.0
        has_played = False

        while True:
            pass
            # try:
            #     if player_state != livingRoomMediaController.status.player_state:
            #         player_state = livingRoomMediaController.status.player_state
            #         print("Player state:", player_state)
            #     if player_state == "PLAYING":
            #         has_played = True
            #     if livingRoomTV.socket_client.is_connected and has_played and player_state != "PLAYING":
            #         has_played = False
            #         livingRoomMediaController.play_media(
            #             premiumVideoLink, "video/mp4")
            #
            #     time.sleep(0.1)
            #     t = t - 0.1
            # except KeyboardInterrupt:
            #     break
            #


if __name__ == "__main__":
    episode = Episode()
    websiteURL = episode.getLatestEpisode()
    premiumVideoLink = episode.getEpisodePremiumVideoLink(websiteURL)
    episode.castEpisodePremiumVideoLink(premiumVideoLink)
