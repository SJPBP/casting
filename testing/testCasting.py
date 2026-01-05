import pychromecast
import time

chromecast, browser = pychromecast.get_listed_chromecasts(
    ["Living Room TV", "Sofa Room TV"])

livingRoomTV = chromecast[0]
sofaRoomTV = chromecast[1]

MEDIA_URL = "https://si.videoapne.to/hls/,bdohxn4p7bboxuzvta474gkxtfyg5xmxxuv6gu7mu46gqsrkennd2qvdyfgq,.urlset/master.m3u8"
LocalURL = ""
print(chromecast)

# Start socket client's worker thread and wait for initial status update
livingRoomTV.wait()

livingRoomTV.quit_app()
# Send media to this object to cast to TV
livingRoomMediaController = livingRoomTV.media_controller

livingRoomMediaController.play_media(
    MEDIA_URL, "application/vnd.apple.mpegurl")
livingRoomMediaController.block_until_active()

player_state = None
t = 30.0
has_played = False

while True:
    try:
        if player_state != livingRoomMediaController.status.player_state:
            player_state = livingRoomMediaController.status.player_state
            print("Player state:", player_state)
        if player_state == "PLAYING":
            has_played = True
        if livingRoomTV.socket_client.is_connected and has_played and player_state != "PLAYING":
            has_played = False
            livingRoomMediaController.play_media(MEDIA_URL, "video/mp4")

        time.sleep(0.1)
        t = t - 0.1
    except KeyboardInterrupt:
        break
