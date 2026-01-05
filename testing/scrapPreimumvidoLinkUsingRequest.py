import requests
from datetime import date
import re
from bs4 import BeautifulSoup

websiteURL = "https://apnetv.biz/Hindi-Serial/show/265754/Taarak-Mehta-Ka-Ooltah-Chashmah"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(websiteURL, headers=headers).text

soup = BeautifulSoup(response, 'lxml')

videoLink = soup.find("div", id="playerwrap").find(
    "script", type="text/javascript")

# Extract Premium link of episode
pattern = r'\"(https?://[^\"]+)\"'
match = re.search(pattern, videoLink.text)

# Check if a match is found and extract the token
if match:
    token = match.group(1)  # Extract the token value
    print(f"Extracted token: {token}")  # Print the token
else:
    print("Token not found.")


# if response.status_code == 200:
#     source = response.text
#     soup = BeautifulSoup(source, 'lxml')
#
#     print(source)
#     # print(soup.prettify())
#     # episodes = soup.find_all("div", class_="shows-box")
#
#     # Gets tmkoc latest episode html data
#     episode = soup.find("div", class_="shows-box")
#
#     # videoOptionLists = episodes.find("span", class_="episode-name").text
#
#     # Get Today date in DDth M YYYY
#     today = date.today()
#     todayDate = today.strftime("%dth %B %Y")
#
#     #
#     episodeVideoUrlsPage = episode.find("a")["href"]
#     episodeDate = episode.find("span", class_="episode-name").text
#
#     if str(todayDate) == str(episodeDate):
#         print("Today Episode is Avaiable")
#         print(episodeVideoUrlsPage)
#         # return episodeVideoUrlsPage
#
#     else:
#         print(f"Latest Episode is of {episodeDate}")
#         print("Today Episode is not Avaiable right now, Please wait")
#
#
# else:
#     print(response.status_code)
#     print(response.content.decode())
#     print("Failed to acces the url")
