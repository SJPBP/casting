from TVShowFetcher import TVShowFetcher

filePath = "/home/fake/Documents/Itti Si Khushi - Main Page.html"
tf = TVShowFetcher(filePath=filePath)

print(tf.get_tv_show())
