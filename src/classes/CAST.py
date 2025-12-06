# from Episode import Episode
from classes.EPISODE import EPISODE
import time

class CAST:
    def __init__(self, episode: EPISODE):
        self.episode = episode
        self.timestamp: int = 0
        self.duration: int = 0

    def update_timestamp(self, timeInSec: int) -> int:
        self.timestamp = timeInSec
        return self.timestamp

    def update_duration(self, duration: int) -> int:
        self.duration = duration
        return self.duration

    def get_time_format_of_timestamp(self, timeInSec = None) -> str:
        if timeInSec:
            return time.strftime('%H:%M:%S', time.gmtime(timeInSec))

        return time.strftime('%H:%M:%S', time.gmtime(self.timestamp))

    def get_time_format_of_duration(self, duration = None) -> str:
        if duration:
            return time.strftime('%H:%M:%S', time.gmtime(duration))

        return time.strftime('%H:%M:%S', time.gmtime(self.duration))

