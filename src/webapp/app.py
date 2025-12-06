from flask import Flask
from tables.Database import Database
from services.ChannelService import ChannelService
from services.TVShowService import TVShowService
from services.EpisodeService import EpisodeService

app = Flask(__name__)

db = Database()
channelService = ChannelService(db)
tVShowService = TVShowService(db)
episodeService = EpisodeService(db)


@app.route("/")
def hello_world():
    return channelService.get_channels()

@app.route("/c")
def get_tv():
    channel = "Sony-TV"
    pageUrl = "https://apnetv.xyz/Channels/Sony-TV"
    channel = channel.replace("-", "_")
    return tVShowService.get_tvshows(channel=channel, pageUrl=pageUrl)

@app.route("/e")
def get_e():
    tvshow = "Chalo Bulawa Aya Hai Mata Ne Bulaya Hai"
    tvshow = tvshow.replace(" ", "_")
    pageUrl = "https://apnetv.xyz/Hindi-Serial/Chalo-Bulawa-Aya-Hai-Mata-Ne-Bulaya-Hai"
    date = "22nd September 2025"

    return episodeService.get_episode(tvshow=tvshow, pageUrl=pageUrl, date=date)

@app.route("/es")
def get_es():
    tvshow = "Chalo Bulawa Aya Hai Mata Ne Bulaya Hai"
    tvshow = tvshow.replace(" ", "_")
    pageUrl = "https://apnetv.xyz/Hindi-Serial/Chalo-Bulawa-Aya-Hai-Mata-Ne-Bulaya-Hai"
    return episodeService.get_episodes(tvshow=tvshow, pageUrl=pageUrl, startNumber=1, endNumber=2)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
