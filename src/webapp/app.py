from flask import Flask, render_template, request
from tables.Database import Database
from classes.CAST import CAST
from classes.EPISODE import EPISODE
from services.ChannelService import ChannelService
from services.TVShowService import TVShowService
from services.EpisodeService import EpisodeService
from caster.Caster import Caster
import time
import requests

app = Flask(__name__)

db = Database()
channelService = ChannelService(db)
tVShowService = TVShowService(db)
caster = Caster()
# cast = None

@app.route("/channels")
def get_channels():
    channels = channelService.get_channels()
    # print(channels)
    # return channels
    return render_template('channels.html', channels=channels["Channels"])


@app.route("/channel/<name>")
def get_channel(name):
    channel = channelService.get_channel(name)
    return channel

@app.route("/tvshows/<channelName>/<path:url>", methods=['GET'])
def get_tvshows(channelName, url):
    channelName = channelName.replace("-", "_")
    print(channelName, url)
    tvshows = tVShowService.get_tvshows(channel=channelName, pageUrl=url)
    print(tvshows)
    return render_template('tvshows.html', tvshows=tvshows["TVShows"])

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

@app.route("/episodes/<string:tvshowName>/<path:url>")
def get_episodes_with_limit(tvshowName, url):
    tvshowName = tvshowName.replace(" ", "_")
    episodeService = EpisodeService(db, tvshowName=tvshowName, pageUrl=url)
    start = 1
    end = 10

    episodes =  episodeService.get_episodes(startNumber=start, endNumber=end)
    return render_template('episodes.html', episodes=episodes["Episodes"][0])


@app.route("/episodes/<string:tvshowName>/<path:url>/<int:start>/<int:end>")
def get_episodes(tvshowName, url, start = None, end = None):
    tvshowName = tvshowName.replace(" ", "_")
    episodeService = EpisodeService(db, tvshowName=tvshowName, pageUrl=url)
        
    episodes =  episodeService.get_episodes(startNumber=start, endNumber=end)
    return render_template('episodes.html', tvshows=episodes["Episodes"])

@app.route("/devices")
def get_devices():
    return {"Devices": ["Living Room TV", "Sofa Room TV"]}

@app.route("/cast/<string:deviceName>", methods=['GET'])
def cast(deviceName="Living Room TV"):
    thumbnail = request.args.get("thumbnail")
    date = request.args.get("date")
    title = request.args.get("title")
    contentUrl = request.args.get("contentUrl")

    caster.find(deviceName)
    caster.connect()

    name = caster.getDeviceName()

    episode = EPISODE(title=title, date=date, thumbnail=thumbnail, contentUrl=contentUrl)
    episode.update_content_type()

    cast_info: CAST = CAST(episode)

    caster.cast(cast_info=cast_info)

    time.sleep(10)

    return render_template('casting.html', casting_device=deviceName)


@app.route("/connect/<string:deviceName>")
def connect(deviceName="Living Room TV"):
    caster.find(deviceName)
    caster.connect()

    return deviceName

@app.route("/pause")
def get_current_time():
    caster.connect()
    timestamp =  caster.get_current_time()
    return timestamp


@app.route("/pause")
def pause():
    caster.connect()
    caster.pause()
    return ""

@app.route("/play")
def play():
    caster.connect()
    caster.play()
    return ""

@app.route("/mute")
def mute():
    caster.connect()
    caster.mute()
    return "Done"

@app.route("/unmute")
def Unmute():
    caster.connect()
    caster.unmute()
    return "done"

@app.route("/quit")
def quit():
    caster.connect()
    caster.quit()
    return "done"



@app.route("/backward")
def backward():
    caster.connect()
    timestamp =  caster.get_current_time()
    if timestamp is not None:
        print(timestamp)
        caster.move_to(timestamp-10)
        pause()
        print(timestamp)
    return "Done"



@app.route("/forward")
def forward():
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
