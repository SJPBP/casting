from flask import Flask
from tables.Database import Database
from classes.CAST import CAST
from services.ChannelService import ChannelService
from services.TVShowService import TVShowService
from services.EpisodeService import EpisodeService
from caster.Caster import Caster
import time

app = Flask(__name__)

db = Database()
channelService = ChannelService(db)
tVShowService = TVShowService(db)
episodeService = EpisodeService(db)
caster = Caster()
cast = None

@app.route("/channels")
def get_channels():
    channels = channelService.get_channels()
    return channels


@app.route("/channel/<name>")
def get_channel(name):
    channel = channelService.get_channel(name)
    return channel

@app.route("/tvshows/<channelName>/<path:url>", methods=['GET'])
def get_tvshows(channelName, url):
    channelName = channelName.replace("-", "_")
    print(channelName, url)
    tvshow = tVShowService.get_tvshows(channel=channelName, pageUrl=url)
    return tvshow

@app.route("/tvshow/<channelName>/<path:url>/<string:tvshowName>", methods=['GET'])
def get_tvshow(channelName, url, tvshowName):
    channelName = channelName.replace("-", "_")
    print(channelName, url, tvshowName)
    tvshow = tVShowService.get_tvshow(channel=channelName, pageUrl=url, name=tvshowName)
    return tvshow

@app.route("/episode/<tvshowName>/<path:url>/<string:date>")
def get_episode(tvshowName, url, date):
    tvshowName = tvshowName.replace(" ", "_")

    episode =  episodeService.get_episode(tvshow=tvshowName, pageUrl=url, date=date)
    return episode

@app.route("/episodes/<string:tvshowName>/<path:url>/<int:start>/<int:end>")
def get_episodes(tvshowName, url, start, end):
    tvshowName = tvshowName.replace(" ", "_")

    episode =  episodeService.get_episodes(tvshow=tvshowName, pageUrl=url, 
                                            startNumber=start, endNumber=end)
    return episode

@app.route("/devices")
def get_devices():
    return {"Devices": ["Living Room TV", "Sofa Room TV"]}

@app.route("/connect/<deviceName>")
def conn_to_tv(deviceName="Living Room TV"):
    global caster
    caster.find(deviceName)
    caster.connect()
    name = caster.getDeviceName()

    return name

@app.route("/cast")
def cast():
    # print(cast.duration)
    get_e()
    conn_to()
    time.sleep(5)
    name = caster.getDeviceName()
    caster.cast(cast)

    return name

@app.route("/pause")
def pause():
    conn_to()
    caster.pause()
    return ""

@app.route("/play")
def play():
    conn_to()
    caster.play()
    return ""

@app.route("/mute")
def mute():
    conn_to()
    caster.mute()
    return "Done"

@app.route("/unmute")
def Unmute():
    conn_to()
    caster.unmute()
    return "done"

@app.route("/forward")
def unmute():
    conn_to()
    timestamp =  caster.get_current_time()
    if timestamp is not None:
        print(timestamp)
        caster.move_to(timestamp+10)
        pause()
        print(timestamp)
    return "Done"

    

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)
