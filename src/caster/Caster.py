import pychromecast
import time

from pychromecast.controllers import media
from pychromecast.discovery import CastBrowser
from classes.CAST import CAST


class Caster:
    def __init__(self):
        self.media_player = None

    def find(self, chromeCastDeviceName: str = ""):
        """
        Locate a Chromecast device on the network.

        Parameters:
        chromeCastDeviceName (str): The name of the Chromecast device to find. 
                             If provided, only this specific device will be identified.

        """
        self.castingDevice = chromeCastDeviceName

        self.chromecast = self.find_Chromecast()


    def find_Chromecast(self) -> pychromecast.Chromecast:
        try:
            # Discover and connect to more than one device
            if self.castingDevice == "":
                chromecasts, _ = pychromecast.get_listed_chromecasts(
                    friendly_names=["Living Room TV", "Sofa Room TV"]
                )

                index = self.ask_user(chromecasts)

                chromecast: pychromecast.Chromecast = chromecasts[index]

            else:
                chromecasts, _ = pychromecast.get_listed_chromecasts(
                    friendly_names=[self.castingDevice]
                )

                chromecast: pychromecast.Chromecast = chromecasts[0]
                
            return chromecast 
        except Exception as e:
            print(e)
            quit()

    def ask_user(self, chromecasts: list[pychromecast.Chromecast]):
        # Ouput options asking for which casting device to use
        print("Available Casting Devices Found:")

        for index,cc in enumerate(chromecasts, start=1):
            print(f"{index}) {cc.cast_info.friendly_name}")

        # Get the device for casting too
        try:
            print("Which Casting Device to use: ", end="")
            index_of_casting_device = int(input()) 
        except KeyboardInterrupt:
            exit()
        
        # List start with 0, not 1
        index_of_casting_device -= 1

        return index_of_casting_device

    def quit(self):
        self.chromecast.quit_app()

    def play(self):
        if self.media_player is not None:
            self.media_player.play()
        else:
            print("Failed")

    def pause(self):
        if self.media_player is not None:
            self.media_player.pause()
        else:
            print("Failed")

    def mute(self):
        if self.media_player is not None:
            self.chromecast.set_volume_muted(True)

    def unmute(self):
        if self.media_player is not None:
            self.chromecast.set_volume_muted(False)

    def move_to(self, timeInSec):
        if self.media_player is not None:
            self.media_player.seek(timeInSec)

    def get_current_time(self) -> float | None:
        try:
            current_time = self.media_player.status.adjusted_current_time
            return current_time
        except:
            print("Failed to get the current time")
            return 0

    def get_duration(self) -> float | None:
        try:
            duration = self.media_player.status.duration
            return duration
        except:
            print("Failed to get the duration of content")
            return 0
    
    def getDeviceName(self) -> str | None:
        try:
            return self.chromecast.cast_info.friendly_name
        except Exception as e:
            print(e)

    def getContentTitle(self) -> str | None:
        try:
            return self.media_player.status.title
        except Exception as e:
            print(e)

    def get_player_status(self) -> bool:
        try:
            player_status = self.media_player.status.player_state
            
            while player_status != "PLAYING" and player_status != "PAUSED":
                player_status = self.media_player.status.player_state
                print(f"Status: {player_status}")
                time.sleep(1)
            return True
        except:
            print("Failed to get player status")
            return False

    def not_connected(self) -> bool:
        """Returns true if not connected to chromecast device"""
        if self.chromecast.app_id != "":
            return False
        else:
            return True
    
    def printStatus(self):
        if self.chromecast == None or self.media_player == None:
            print("Please connect to chromecast device that has something playing on it")
            return False
        print(self.chromecast.status)
        print(self.chromecast.status_event)
        print(self.media_player.status)

    def connect(self):
        # Already connected to TV
        if self.media_player is not None:
            return True
        print("Connecting to TV")
        # Not connected to TV

        cast: pychromecast.Chromecast = self.chromecast

        # Start worker thread and wait for cast device to be ready
        cast.wait()

        # Media controller which casting to device
        self.media_player = cast.media_controller

        self.media_player.block_until_active(2.0)
        print("Connected")

    def cast(self, cast_info: CAST):
        print("Casting to TV")
        cast: pychromecast.Chromecast = self.chromecast
                # Start worker thread and wait for cast device to be ready
        cast.wait()

        # Stop any media playing on the device
        cast.quit_app()

        # Media controller which casting to device
        self.media_player = cast.media_controller
        
        print(cast_info.episode)

        self.media_player.play_media(
                url=cast_info.episode.contentUrl, 
                content_type=cast_info.episode.contentType, 
                current_time=cast_info.timestamp,
                title=cast_info.episode.title,
                thumb=cast_info.episode.thumbnail
        )
        self.media_player.block_until_active()

        time.sleep(1)
        print("Casting Now")


    
if __name__ == "__main__":
    URL = "https://si.videoapne.to/bdohxy5m7bboxuzvta5p4gqvtqipmm7gm36svw2vdbeu6gdhdq2ycw3x3vua/v.mp4"
    URL = "https://s2.videoapne.to/hls/,bdohwygw7bboxuzvta574eqltc3dzxtncki6twj6xgsjbtxy2vvzpbex6z4a,.urlset/master.m3u8"
    # URL = "https://si.videoapne.to/bdohwrow7bboxuzvta574fif3ioqycxvz3zlm35j6sf6vloxgnadx7vd5fvq/v.mp4"
    # cast = Caster(URL, timeStamp=0, content_type="application/x-mpegurl", title="Bigg Boss 19")
    # cast.find("Living Room TV") 
    # cast.cast()
    # cast.reconnect()
    # print(cast.chromecast.app_id)

    # while cast.not_connected():
    #     pass
    # time.sleep(10)
    #
    # print(cast.getDeviceName())
    # print(cast.getContentTitle())

    
