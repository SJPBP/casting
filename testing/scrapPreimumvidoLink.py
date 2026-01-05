import requests
import re
from bs4 import BeautifulSoup

with open("./Taarak Mehta Ka Ooltah Chashmah 19th March online - WITH Video.html") as episodeFile:
    soup = BeautifulSoup(episodeFile, 'lxml')

# Source: https://stackoverflow.com/a/26192778
videoLink = soup.find("div", id="playerwrap").find("script", type="text/javascript")

# Extract Premium link of episode
pattern = r'\"(https?://[^\"]+)\"'
match = re.search(pattern, videoLink.text)

# Check if a match is found and extract the token
if match:
    token = match.group(1)  # Extract the token value
    print(f"Extracted token: {token}")  # Print the token
else:
    print("Token not found.")

