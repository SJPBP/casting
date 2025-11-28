from tables.Database import Database
from classes.EPISODE import EPISODE

class EpisodeTable:
    def __init__(self, db: Database, tvshowName: str) -> None:
        self.db = db 
        self.name = tvshowName
        self.createTable()
    
    def createTable(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.name} (
                    date DATE PRIMARY KEY, 
                    link VARCHAR(500),
                    title VARCHAR(500),
                    type VARCHAR(100),
                    thumbnail VARCHAR(500)
                    );
        """
        self.db.execute(sql)
    
    def insert_all(self, episodes: list[EPISODE]) -> list[EPISODE] | None:
        """Insert all episodes in list"""
        index = 1
        for episode in episodes:
            print(f"Adding episode {index}...")

            sql = f"""
                INSERT INTO {self.name} (date, link, title, type, thumbnail)
                VALUES (%s, %s, %s, %s, %s);  
                """

            self.db.execute(sql, params=(episode.convert_date_to_mysql_format(), episode.contentUrl, episode.title, episode.contentType, episode.thumbnail,))

            index += 1
            
        return episodes

    def insert(self, episode: EPISODE):
        sql = f"""
           INSERT INTO {self.name} (date, link, title, type, thumbnail)
                VALUES (%s, %s, %s, %s, %s); 
        """

        self.db.execute(sql, params=(episode.convert_date_to_mysql_format(),episode.contentUrl, episode.title, episode.contentType, episode.thumbnail,))
    
    def get_all(self) -> list[EPISODE] | None:
        """Return all the data inside the database"""
        sql = f"""
            SELECT * FROM {self.name};
        """

        rows = self.db.execute(sql, params=None, fetchall=True)

        if not rows:
            return None

        episodes = []

        for row in rows:
            episode = EPISODE(date=row["date"], thumbnail=row["thumbnail"], contentUrl=row["link"], contentType=row["type"], title=row["title"])
            episodes.append(episode)

        return episodes


    def get_by_date(self, date: str):
        episode = EPISODE(date=date)

        sql = f"""
           SELECT date, link, title, type, thumbnail from {self.name} WHERE date = (%s);
        """

        row = self.db.execute(sql, params=(episode.convert_date_to_mysql_format(),), fetchall=True)

        if not row:
            return None

        row = row[0]
        
        return EPISODE(
            date=row["date"], 
            thumbnail=row["thumbnail"], 
            contentUrl=row["link"], 
            contentType=row["type"],
            title=row["title"]
                       )

    def delete(self, episode: EPISODE):
        sql = f"""
        DELETE FROM {self.name}
        WHERE date = (%s);
        """

        self.db.execute(sql, params=(episode.get_date_in_mysql_format(),))

    def update(self, episode: EPISODE):
        sql = f"""
        UPDATE {self.name}
        SET link, title, type, thumbnail (%s) WHERE date = (%s);
        """

        self.db.execute(sql, params=(episode.contentUrl, episode.title, episode.contentType, episode.thumbnail, episode.get_date_in_mysql_format(),))


