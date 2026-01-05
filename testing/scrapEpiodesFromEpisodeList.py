import requests
from bs4 import BeautifulSoup
from datetime import date

with open("./updatedTmkocEpisodesLists.html") as episodeFile:
    soup = BeautifulSoup(episodeFile, 'lxml')

# print(soup.prettify())
# episodes = soup.find_all("div", class_="shows-box")
episodes = soup.find_all("div", class_="shows-box")
# videoOptionLists = episodes.find("span", class_="episode-name").text

for episode in episodes:
    # Get Today date in DDth M YYYY
    today = date.today()
    todayDate = today.strftime("%dth %B %Y")

    episodesListsPage = episode.find("a")["href"]
    videoOptionLists = episode.find("span", class_="episode-name").text

    if str(todayDate) == str(videoOptionLists):
        print("Today Episode is Avaiable")
        print(episodesListsPage)
    else:
        print(f"Latest Episode is of {videoOptionLists}")
        print("Today Episode is not Avaiable right now, Please wait")
