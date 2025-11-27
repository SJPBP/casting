from Database import Database
from dataclasses.EPISODE import EPISODE

class EpisodeTable:
    def __init__(self, db: Database) -> None:
        self.db = db 

    def createTable(self, episode: EPISODE):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {episode.name} (
                    date DATE PRIMARY KEY, 
                    link VARCHAR(1000),
                    type VARCHAR(100),
                    thumbnail VARCHAR(1000)
                    );
        """
        self.db.execute(sql)
    
    def insert(self, episode: EPISODE):
        sql = f"""
           INSERT INTO {episode.name} (date, link, type, thumbnail)
                VALUES (%s, %s, %s, %s); 
        """

        self.db.execute(sql, params=(episode.date, episode.contentUrl, episode.contentType, episode.thumbnail,))

    def get_by_date(self, episode: EPISODE):
        sql = f"""
           SELECT link, type, thumbnail from {episode.name} WHERE date = (%s);
        """

        row = self.db.execute(sql, params=(episode.date,), fetchall=True)

        if not row:
            return None
        return EPISODE(name=episode.name, 
                       date=episode.date, 
                       thumbnail=row["thumbnail"], 
                       contentUrl=row["link"], 
                       contentType=row["type"],
                       title=None)

    def delete(self, episode: EPISODE):
        sql = f"""
        DELETE FROM {episode.name}
        WHERE date = (%s);
        """

        self.db.execute(sql, params=(episode.date,))

    def update(self, episode: EPISODE):
        sql = f"""
        UPDATE {episode.name}
        SET mp4_link = (%s) WHERE date = (%s);
        """

        self.db.execute(sql, params=(episode.contentUrl, episode.date,))


