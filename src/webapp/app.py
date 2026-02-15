import time

from flask import Flask, redirect, render_template, request

from caster.Caster import Caster
from classes.CAST import CAST
from classes.EPISODE import EPISODE
from services.ChannelService import ChannelService
from services.EpisodeService import EpisodeService
from services.TVShowService import TVShowService
from tables.Database import Database

app = Flask(__name__)

db = Database()
channelService = ChannelService(db)
tVShowService = TVShowService(db)
caster = Caster()
# cast = None


@app.route("/")
def home():
    return redirect("/channels")


@app.route("/channels")
def get_channels():
    channels = channelService.get_channels()
    # return channels
    return render_template("channels.html", channels=channels["Channels"])


@app.route("/channel/<name>")
def get_channel(name):
    channel = channelService.get_channel(name)
    return channel


@app.route("/tvshows/<channelName>/<path:url>", methods=["GET"])
def get_tvshows(channelName, url):
    channelName = channelName.replace("-", "_")
    tvshows = tVShowService.get_tvshows(channel=channelName, pageUrl=url)
    return render_template("tvshows.html", tvshows=tvshows["TVShows"])

    return tvshow


@app.route("/tvshow/<channelName>/<path:url>/<string:tvshowName>", methods=["GET"])
def get_tvshow(channelName, url, tvshowName):
    channelName = channelName.replace("-", "_")
    tvshow = tVShowService.get_tvshow(channel=channelName, pageUrl=url, name=tvshowName)
    return tvshow


@app.route("/episode/<tvshowName>/<path:url>/<string:date>")
def get_episode(tvshowName, url, date):
    tvshowName = tvshowName.replace(" ", "_")

    episode = episodeService.get_episode(tvshow=tvshowName, pageUrl=url, date=date)
    return episode


@app.route("/episodes/<string:tvshowName>/<path:url>/<int:page>")
def get_episodes_with_limit(tvshowName, url, page):
    if page <= 0:
        page = 1
    tvshowName = tvshowName.replace(" ", "_")
    episodeService = EpisodeService(db, tvshowName=tvshowName, pageUrl=url)
    end = page * 10
    start = end - 9

    episodes = episodeService.get_episodes(startNumber=start, endNumber=end)
    return render_template("episodes.html", episodes=episodes["Episodes"][0])


@app.route("/episodes/<string:tvshowName>/<path:url>/<int:start>/<int:end>")
def get_episodes(tvshowName, url, start=None, end=None):
    tvshowName = tvshowName.replace(" ", "_")
    episodeService = EpisodeService(db, tvshowName=tvshowName, pageUrl=url)

    episodes = episodeService.get_episodes(startNumber=start, endNumber=end)
    return render_template("episodes.html", tvshows=episodes["Episodes"])


@app.route("/devices")
def get_devices():
    return {"Devices": ["Living Room TV", "Sofa Room TV"]}


@app.route("/cast/<string:deviceName>", methods=["GET"])
def cast(deviceName="Living Room TV"):
    thumbnail = request.args.get("thumbnail")
    date = request.args.get("date")
    title = request.args.get("title")
    contentUrl = request.args.get("contentUrl")

    caster.find(deviceName)
    caster.connect()

    name = caster.getDeviceName()

    episode = EPISODE(
        title=title, date=date, thumbnail=thumbnail, contentUrl=contentUrl
    )
    episode.update_content_type()

    cast_info: CAST = CAST(episode)

    caster.cast(cast_info=cast_info)

    time.sleep(10)

    return render_template("media_player.html", device=deviceName)


@app.route("/test_cast", methods=["GET"])
def test_cast_html():
    return render_template("casting.html", casting_device="Living Room TV")


@app.route("/connect/<string:deviceName>")
def connect(deviceName="Living Room TV"):
    caster.find(deviceName)
    caster.connect()

    return deviceName


@app.route("/pause")
def pause():
    device_name = request.args.get("device_name")
    connect(device_name)
    caster.pause()
    return "Done"


@app.route("/play")
def play():
    device_name = request.args.get("device_name")
    print(device_name)
    connect(device_name)
    caster.play()
    return ""


@app.route("/mute")
def mute():
    device_name = request.args.get("device_name")
    print(device_name)
    connect(device_name)

    caster.mute()

    return "Done"


@app.route("/unmute")
def Unmute():
    device_name = request.args.get("device_name")
    print(device_name)
    connect(device_name)

    caster.unmute()

    return "done"


@app.route("/quit")
def quit():
    device_name = request.args.get("device_name")
    print(device_name)
    connect(device_name)

    caster.quit()

    return "done"


@app.route("/current_time")
def current_time():
    device_name = request.args.get("device_name")
    print(device_name)
    connect(device_name)
    timestamp = caster.get_current_time()
    return f"{timestamp}"


@app.route("/backward")
def backward():
    seek = request.args.get("time")
    if seek is None:
        seek = 10

    device_name = request.args.get("device_name")
    print(device_name)
    connect(device_name)

    timestamp = caster.get_current_time()

    if timestamp is not None:
        caster.move_to(timestamp - seek)
        pause()

    return "Done"


@app.route("/forward", methods=["GET"])
def forward():
    seek = request.args.get("time")
    if seek is None:
        seek = 10

    device_name = request.args.get("device_name")
    print(device_name)
    connect(device_name)

    timestamp = caster.get_current_time()
    if timestamp is not None:
        caster.move_to(timestamp + seek)
        pause()
    return "Done"


# main driver function
if __name__ == "__main__":

    # run() method of Flask class runs the application
    # on the local development server.
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
