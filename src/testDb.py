import mysql.connector

from dataclasses.EPISODE import EPISODE
from tables.EpisodeTable import EpisodeTable
from Database import Database



showName = "Bigg-Boss-19"
showName = showName.replace("-", "_")
link = "https://s2.videoapne.to/bdohxcg57bboxuzvta574dky3ue7hdhoaxkar6ggbviypdrduup7vbgpvrba/v.mp4"
date = "2025-11-21"
thumbnail = "https://s2.videoapne.to/i/01/00023/p93ykf6yaw6k.jpg?xyz"
title = showName.replace("-", " ")  + " - " + date.replace("-", "/")
contentType = link.split(".")[-1]
tvShow = EPISODE(name=showName, date=date, thumbnail=thumbnail, contentUrl=link, title=title, contentType=contentType)

db = Database()

bb = EpisodeTable(db)
bb.createTable(tvShow)
bb.insert(tvShow)

print(bb.get_by_date(tvShow))

# print(tvShow)
# db = mysql.connector.connect(user='cast', password='171995',
#                               host='127.0.0.1',
#                              port="3307",
# 	                      database='ApneTV')
#
# cursor = db.cursor() 
#
# cursor.execute("SELECT * FROM test;")
#
# m = cursor.fetchall()
# print(m)
# # print(m[0])
# # print(m[0][0])
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS Colors (
#                     tv_show_id VARCHAR(768) PRIMARY KEY NOT NULL,
#                     tv_show_name VARCHAR(10000) NOT NULL, 
#                     tv_show_thumbnail VARCHAR(10000) NOT NULL,
#                     total VARCHAR(10000) NOT NULL
#                     );""")
#
# db.close() 
