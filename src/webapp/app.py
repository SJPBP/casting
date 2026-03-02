from flask import Flask, redirect, render_template, request

from caster.Caster import Caster
from caster.Player import Player
from classes.CAST import CAST
from classes.EPISODE import EPISODE
from services.ChannelService import ChannelService
from services.EpisodeService import EpisodeService
from services.TimerService import TimerService
from services.TVShowService import TVShowService
from tables.Database import Database

app = Flask(__name__)

db = Database()
channelService = ChannelService(db)
tVShowService = TVShowService(db)
caster = Caster()
# cast = None

devices = {}
timer = TimerService()

storeEpisodes = {}

# obj created by getting chromecast device
# It will have self.cast = pychromecast.get_chromecasts()[0]

# To check if media is playing on TV
# I have a background method which will change self.is_media_playing

# if self.media.is_playing
# yes
# I will get self.media.title
# And check if it my media I want to play

# Yes, do nothing more
# No, cast my media
# No
# Cast my media
# Both no is casting so I should do something about this


# Then I will put device_1 into devices dict


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


@app.route("/episodes")
def get_episodes_with_limit():
    timer.start_timer("episodes")

    tvshowName = request.args.get("tvshowName")

    url = request.args.get("url")

    page: int = int(request.args.get("page"))

    if page <= 0 or page is None:
        page = 1

    tvshowName = tvshowName.replace(" ", "_")
    if tvshowName in storeEpisodes:
        episodeService = storeEpisodes[tvshowName]
    else:
        episodeService = EpisodeService(db, tvshowName=tvshowName, pageUrl=url)
        storeEpisodes[tvshowName] = episodeService

    print("***" * 20)

    end = page * 10
    start = end - 9

    episodes = episodeService.get_episodes(startNumber=start, endNumber=end)

    total_time = timer.end_timer("episodes")

    print(f"Getting episodes took {total_time} seconds")

    return render_template("episodes.html", episodes=episodes["Episodes"][0], page=page)


@app.route("/episodes/<string:tvshowName>/<path:url>/<int:start>/<int:end>")
def get_episodes(tvshowName, url, start=None, end=None):
    tvshowName = tvshowName.replace(" ", "_")
    episodeService = EpisodeService(db, tvshowName=tvshowName, pageUrl=url)

    episodes = episodeService.get_episodes(startNumber=start, endNumber=end)
    return render_template("episodes.html", tvshows=episodes["Episodes"])


@app.route("/devices")
def get_devices():
    return {"Devices": ["Living Room TV", "Sofa Room TV"]}


def connect_chromecast(deviceName):
    if deviceName in devices:
        print("Already connected to device")
        player = devices[deviceName]
    else:
        print("Creating connection to device")
        player = Player(deviceName)
        devices[deviceName] = player

    return player


@app.route("/cast/<string:deviceName>", methods=["GET"])
def cast(deviceName="Living Room TV"):
    thumbnail = request.args.get("thumbnail")
    date = request.args.get("date")
    title = request.args.get("title")
    contentUrl = request.args.get("contentUrl")

    player = connect_chromecast(deviceName)
    episode = EPISODE(
        title=title, date=date, thumbnail=thumbnail, contentUrl=contentUrl
    )

    # Get ext of content
    episode.update_content_type()
    # Make title unqiue by adding title
    episode.add_date_to_title()

    cast_info: CAST = CAST(episode)

    print("CASTING TO TV")
    player.cast(cast_info)
    return render_template("media_player.html")


# @app.route("/cast/<string:deviceName>", methods=["GET"])
# def to_be_deleted_cast(deviceName="Living Room TV"):
#     thumbnail = request.args.get("thumbnail")
#     date = request.args.get("date")
#     title = request.args.get("title")
#     contentUrl = request.args.get("contentUrl")
#
#     caster.find(deviceName)
#     caster.connect()
#
#     name = caster.getDeviceName()
#

#
#     caster.cast(cast_info=cast_info)
#
#     time.sleep(10)
#
#     return render_template("media_player.html", device=deviceName)


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
    player = connect_chromecast(device_name)
    # connect(device_name)
    # caster.pause()
    player.pause()
    return "Pause"


@app.route("/play")
def play():
    device_name = request.args.get("device_name")
    player = connect_chromecast(device_name)
    player.play()
    # print(device_name)
    # connect(device_name)
    # caster.play()
    return "Playing"


@app.route("/mute")
def mute():
    device_name = request.args.get("device_name")
    # print(device_name)
    # connect(device_name)
    player = connect_chromecast(device_name)
    player.mute()

    # caster.mute()

    return "Done"


@app.route("/unmute")
def Unmute():
    device_name = request.args.get("device_name")
    # print(device_name)
    # connect(device_name)

    # caster.unmute()
    player = connect_chromecast(device_name)
    player.unmute()
    return "done"


@app.route("/quit")
def quit():
    device_name = request.args.get("device_name")
    # print(device_name)
    # connect(device_name)
    #
    player = connect_chromecast(device_name)
    player.caster.quit()

    return "done"


@app.route("/get_current_time")
def get_current_time():
    device_name = request.args.get("device_name")
    player = connect_chromecast(device_name)
    timestamp = player.get_current_time()
    # print(device_name)
    # connect(device_name)
    if timestamp is not None:
        return f"{timestamp}"
    else:
        return "Not playing any media!"


@app.route("/set_current_time")
def set_current_time():
    device_name = request.args.get("device_name")
    seek = float(request.args.get("timestamp"))

    player = connect_chromecast(device_name)
    if seek is None:
        player.set_current_time(442.012336)
    else:
        player.set_current_time(seek)

    # device_name = request.args.get("device_name")
    # print(device_name)
    # connect(device_name)
    #
    # timestamp = caster.get_current_time()
    #
    # if timestamp is not None:
    #     caster.move_to(timestamp - seek)
    #     pause()

    return "Done"


@app.route("/backward")
def backward():
    device_name = request.args.get("device_name")
    seek = request.args.get("timestamp")

    player = connect_chromecast(device_name)
    timestamp = player.get_current_time()
    player.backward_media_by(timestamp)

    return "Done"


@app.route("/forward", methods=["GET"])
def forward():
    device_name = request.args.get("device_name")
    seek = request.args.get("amount")

    player = connect_chromecast(device_name)
    timestamp = player.get_current_time()
    player.forward_media_by(timestamp)

    return "Done"


# main driver function
if __name__ == "__main__":

    # run() method of Flask class runs the application
    # on the local development server.
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
