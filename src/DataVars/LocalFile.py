from bs4 import BeautifulSoup


class LocalFile:
    def __init__(self, localFile=None):
        self.localFile = localFile
        self.htmlData = None

    def getWebsiteSourceFromLocalFile(self) -> None:
        '''Get the html data from local html file and store it in htmlData'''
        if self.localFile == None:
            with open(self.localFile) as episodeFile:
                soup = BeautifulSoup(episodeFile, 'lxml')
        else:
            print("Please give local html file")



