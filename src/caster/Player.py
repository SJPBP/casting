from time import sleep

import pychromecast

from caster.Caster import Caster


class Player:
    def __init__(self, device_name: str) -> None:
        self.device_name: str = device_name
        self.caster = Caster()
        self.chromecast_obj: pychromecast.Chromecast = self.get_chromecast_of(
            device_name
        )
        self.wait_for_connect_to_tv()

    def get_chromecast_of(self, device_name: str) -> pychromecast.Chromecast:
        chromecast = self.caster.find(device_name)

        return chromecast

    def wait_for_connect_to_tv(self):
        self.caster.connect(self.chromecast_obj)
        print("WAITING FOR TV TO CONNECT")
        while self.caster.getContentTitle() is None:
            print(self.caster.getContentTitle())
            sleep(0.2)

    def cast(self, cast_info):
        # Get the title of media playing on tv
        title_of_media_playing_on_tv = self.caster.getContentTitle()
        print(f"TITLE OF MEDIA PLAYING ON TV: {title_of_media_playing_on_tv}")
        sleep(2)
        # Check if there is media playing on tv
        # and it is the I trying to cast
        if (
            title_of_media_playing_on_tv is not None
            and cast_info.episode.title == title_of_media_playing_on_tv
        ):
            return True
        else:
            # Either there is no media playing or different media from what I trying to cast
            self.caster.cast(cast_info)

    def status(self) -> dict:
        status = {
            "Playing": f"{self.is_playing()}",
            "Muted": f"{self.is_muted()}",
            "Volume": f"{self.get_volume_level()}",
            "Timestamp": f"{self.get_current_time()}",
        }

        return status

    def play(self):
        self.caster.play()

    def is_playing(self) -> bool:
        return self.caster.is_media_playing()

    def is_muted(self) -> bool:
        return self.caster.is_muted()

    def pause(self):
        self.caster.pause()

    def mute(self):
        self.caster.mute()

    def unmute(self):
        self.caster.unmute()

    def backward_media_by(self, timestamp, seek_seconds: int = 10):
        amount_back_in_sec = timestamp - seek_seconds

        self.caster.move_to(amount_back_in_sec)

    def forward_media_by(self, timestamp, seek_seconds: int = 10):
        amount_forward_in_sec = timestamp + seek_seconds

        self.caster.move_to(amount_forward_in_sec)

    def get_current_time(self) -> float | None:
        timestamp_in_seconds = self.caster.get_current_time()

        # There nothing running on TV so there is no timestamp
        if timestamp_in_seconds is None:
            return None
        else:
            return timestamp_in_seconds

    def set_current_time(self, timestamp_in_seconds: float):
        self.caster.move_to(timestamp_in_seconds)

    def get_volume_level(self) -> float:
        return self.caster.get_volume()

    def set_volume_level(self, amount_in_float):
        self.caster.set_volume(amount_in_float)
