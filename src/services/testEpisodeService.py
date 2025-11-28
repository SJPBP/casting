from services.EpisodeService import EpisodeService
from tables.Database import Database


db = Database()
eps = EpisodeService(db, "Chalo_Bulawa_Aya_Hai_Mata_Ne_Bulaya_Hai")
pageUrl = "https://apnetv.xyz/Hindi-Serial/Chalo-Bulawa-Aya-Hai-Mata-Ne-Bulaya-Hai"
print(eps.get_episodes(pageUrl=pageUrl, 
                       numberOfEpisodes=3))

# print(eps.get_episode(pageUrl=pageUrl, date="24th November 2025"))
