from tables.Database import Database
from classes.TVSHOW import TVSHOW

class TvShowTable:
    def __init__(self, db: Database, channel: str) -> None:
        self.db = db 
        self.channel = channel
        self.createTable()

    def createTable(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.channel} (
                    name VARCHAR(500) PRIMARY KEY,
                    channel VARCHAR(500),
                    thumbnail VARCHAR(500),
                    page_url VARCHAR(500) NULL,
                    description VARCHAR(500) NULL,
                    totalEpisodes INT
                    );
        """
        self.db.execute(sql)
    
    def insert_all(self, tvshows: list[TVSHOW]) -> list[TVSHOW] | None:
        """Insert all channels in list"""
        index = 1
        for tvshow in tvshows:
            print(f"Adding tvshow {index}...")

            sql = f"""
               INSERT INTO {self.channel} (name, channel, thumbnail, page_url, description, totalEpisodes)
                    VALUES (%s, %s, %s, %s, %s, %s);
            """

            self.db.execute(sql, params=(tvshow.name, tvshow.channel, tvshow.thumbnail, tvshow.pageUrl, tvshow.description,tvshow.totalEpisodes,))

            index += 1
            
        return tvshows

    def insert(self, tvShow: TVSHOW):
        sql = f"""
           INSERT INTO {self.channel} (name, channel, thumbnail, page_url, description, totalEpisodes)
                VALUES (%s, %s, %s, %s, %s, %s);
        """

        self.db.execute(sql, params=(tvShow.name, tvShow.channel, tvShow.thumbnail, tvShow.pageUrl, tvShow.description, tvShow.totalEpisodes,))
    
    def get_all(self, channel: str) -> TVSHOW:
        """Return all the data inside the database"""
        sql = f"""
            SELECT * FROM {self.channel};
        """

        rows = self.db.execute(sql, params=None, fetchall=True)

        if not rows:
            return None

        tvshows: list[TVSHOW] = []

        for row in rows:
            tvshow = TVSHOW(channel=row["channel"], 
                      name=row["name"], 
                      thumbnail=row["thumbnail"], 
                      pageUrl=row["page_url"],
                      description=row["description"],
                      totalEpisodes=row["totalEpisodes"]
                      )

            tvshows.append(tvshow)

        return tvshows


    def get_by_channel(self, tvShow: TVSHOW):
        sql = f"""
           SELECT name, channel, thumbnail, page_url, description, totalEpisodes from {self.channel} WHERE name = (%s);
        """

        row = self.db.execute(sql, params=(tvShow.name,), fetchall=True)

        if not row:
            return None
        row = row[0]
        return TVSHOW(channel=row["channel"], 
                      name=row["name"], 
                      thumbnail=row["thumbnail"], 
                      pageUrl=row["page_url"],
                      description=row["description"],
                      totalEpisodes=row["totalEpisodes"]
                      )

    def delete(self, tvShow: TVSHOW):
        sql = f"""
        DELETE FROM {tvShow.channel}
        WHERE name = (%s);
        """

        self.db.execute(sql, params=(tvShow.name,))

    def update(self, tvShow: TVSHOW):
        sql = f"""
        UPDATE {self.channel}
        SET channel = (%s), thumbnail = (%s), page_url = (%s), description = (%s), totalEpisodes = (%s) WHERE name = (%s);
        """

        self.db.execute(sql, params=(tvShow.channel, tvShow.thumbnail, tvShow.pageUrl, tvShow.description, tvShow.totalEpisodes, tvShow.name,))
