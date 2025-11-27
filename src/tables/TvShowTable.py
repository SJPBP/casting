from Database import Database
from TVSHOW import TVSHOW

class TvShowTable:
    def __init__(self, db: Database) -> None:
        self.db = db 

    def createTable(self, tvShow: TVSHOW):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {tvShow.channel} (
                    name VARCHAR(1000) PRIMARY KEY,
                    channel VARCHAR(1000),
                    thumbnail VARCHAR(1000),
                    description VARCHAR(1000) NULL,
                    );
        """
        self.db.execute(sql)
    
    def insert(self, tvShow: TVSHOW):
        sql = f"""
           INSERT INTO {tvShow.channel} (name, channel, thumbnail, description)
                VALUES (%s, %s, %s); 
        """

        self.db.execute(sql, params=(tvShow.name, tvShow.channel, tvShow.thumbnail, tvShow.description,))

    def get_by_channel(self, tvShow: TVSHOW):
        sql = f"""
           SELECT name, channel, thumbnail, description from {tvShow.channel} WHERE name = (%s);
        """

        row = self.db.execute(sql, params=(tvShow.name,), fetchall=True)

        if not row:
            return None
        return TVSHOW(channel=row["channel"], 
                      name=row["name"], 
                      thumbnail=row["thumbnail"], 
                      description=row["description"])

    def delete(self, tvShow: TVSHOW):
        sql = f"""
        DELETE FROM {tvShow.channel}
        WHERE name = (%s);
        """

        self.db.execute(sql, params=(tvShow.name,))

    def update(self, tvShow: TVSHOW):
        sql = f"""
        UPDATE {tvShow.channel}
        SET thumbnail = (%s), description = (%s) WHERE name = (%s);
        """

        self.db.execute(sql, params=(tvShow.thumbnail, tvShow.description, tvShow.name,))
