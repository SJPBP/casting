#TODO: I will go to page of channel, using url to page
#TODO: I will get the channel name, logo (download it)
#TODO: Then I will create object of TVShow for new and old shows, and add it to list.
#TODO: Before adding to list, object will be populated on its own.

# from Episode import Episode
from dataclasses import dataclass

@dataclass
class TVSHOW:
    channel: str 
    name: str
    thumbnail: str
    totalEpisodes: int
    pageUrl: str
    # None = None means set default value to None like name: str | None = None
    description: str 

    @property
    def json(self):
        return  {
            "Channel": self.channel,
            "Name": self.name,
            "Thumbnail": self.thumbnail,
            "TotalEpisodes": self.totalEpisodes,
            "PageUrl": self.pageUrl,
            "Description": self.description
        }
