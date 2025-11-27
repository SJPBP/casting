import argparse
from scrapers.ChannelScraper import ChannelScraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backend to Casting")
    parser.add_argument("-gcs", "--get-channels", action="store_true", help="Return JSON of Channels")
    parser.add_argument("-gc", "--get-channel", help="Return JSON of Channel Name")
    parser.add_argument("-gtvs", "--get-tvshows", help="Return JSON of TvShows")
    args = parser.parse_args()

    filePath = "/home/fake/Documents/ApneTV_Home_Page.html"
    channels = ChannelScraper(filePath=filePath)

    if args.get_channels:
        print(channels.get_channels())

    if args.get_channel:
        print(channels.get_channel(args.get_channel))

        


            


