#TODO: I will go to page of channel, using url to page
#TODO: I will get the channel name, logo (download it)
#TODO: Then I will create object of TVShow for new and old shows, and add it to list.
#TODO: Before adding to list, object will be populated on its own.

# from Episode import Episode
from dataclasses import dataclass

@dataclass
class CHANNEL:
    name: str
    logoUrl: str 
    pageUrl: str
    id: int | None = None

    @property
    def json(self):
        return  {
            "name": self.name, 
             "logoUrl": self.logoUrl,
             "pageUrl": self.pageUrl,
             "id": self.id
        }

