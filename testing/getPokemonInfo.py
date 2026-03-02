import requests
import json

baseUrl = "https://pokeapi.co/api/v2/"


def getPokemonInfo(pokemonName: str) -> dict:
    url = f"{baseUrl}/pokemon/{pokemonName}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemonData = response.json()
        return pokemonData
    else:
        print(f"Failed to retrieve data {response.status_code}")


pokemonName = "pikachu"
pokemonInfo = getPokemonInfo(pokemonName)

if pokemonInfo:
    # print(json.dumps(pokemonInfo, indent=2))
    print(f"{pokemonInfo["name"]}")
    print(f"{pokemonInfo["id"]}")
    print(f"{pokemonInfo["height"]}")
