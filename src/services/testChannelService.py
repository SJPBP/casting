from services.ChannelService import ChannelService
from tables.Database import Database
from classes.CHANNEL import CHANNEL

db = Database()

chans = ChannelService(db)

# chans.get_channel()
print(chans.get_channels())
print(chans.get_channel("Colors"))
