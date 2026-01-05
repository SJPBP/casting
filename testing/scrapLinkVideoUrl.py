import requests
import re
from bs4 import BeautifulSoup

with open("./Understanding Money Sanctions in Global Finance.html") as episodeFile:
    soup = BeautifulSoup(episodeFile, 'lxml')

# Source: https://stackoverflow.com/a/26192778
videoLink = soup.find("div", id='single_player').find("iframe")["src"]

# Extract Premium link of episode
pattern = r'\?url=([^\&]+)'
match = re.search(pattern, videoLink)

# Check if a match is found and extract the token
if match:
    token = match.group(1)  # Extract the token value
    print(f"Extracted token: {token}")  # Print the token
else:
    print("Token not found.")

