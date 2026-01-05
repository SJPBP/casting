import requests

response = requests.get("https://xkcd.com/353/")

if response.status_code == 200:
    print(f"Response: {response.text}")
else:
    print(f"Failed to get Data {response}")
