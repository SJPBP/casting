from services.TVShowService import TVShowService
from tables.Database import Database


db = Database()
tvs = TVShowService(db, "Sony_TV")
print(tvs.get_tvshows("https://apnetv.xyz/Channels/Sony-TV"))


