from scrapers.TVShowFetcher import TVShowFetcher

filePath = "/home/fake/Documents/Itti Si Khushi - Main Page.html"
tf = TVShowFetcher(filePath=filePath)

tf.get_tv_show()
