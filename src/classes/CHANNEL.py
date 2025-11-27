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

    def __str__(self):
        return {'ChannelName': f'{self.name}', 'channelIcon': f'{self.logoUrl}', 'pageUrl': f'{self.pageUrl}'}

    def __repr__(self):
        return {'ChannelName': f'{self.name}', 'channelIcon': f'{self.logoUrl}', 'pageUrl': f'{self.pageUrl}'}
