from services.EpisodeService import EpisodeService
from tables.Database import Database


db = Database()
pageUrl = "https://apnetv.xyz/Hindi-Serial/Chalo-Bulawa-Aya-Hai-Mata-Ne-Bulaya-Hai"
# print(eps.get_episodes(pageUrl=pageUrl, 
                       # numberOfEpisodes=3))
# eps.shallow_search(tvshowName="Chalo_Bulawa_Aya_Hai_Mata_Ne_Bulaya_Hai", pageUrl=pageUrl)
tvshowName = "Chalo_Bulawa_Aya_Hai_Mata_Ne_Bulaya_Hai"
eps = EpisodeService(db, tvshowName=tvshowName, pageUrl=pageUrl)

# print(eps.get_episodes(startNumber=3, endNumber=3))
print(eps.get_episode("13th November 2025"))

# print(eps.get_episode(pageUrl=pageUrl, date="24th November 2025"))
