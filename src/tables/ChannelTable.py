from Database import Database
from dataclasses.CHANNEL import CHANNEL

class ChannelTable:
    def __init__(self, db: Database) -> None:
        self.db = db 

    def createTable(self, channel: CHANNEL):
        sql = f"""
            CREATE TABLE IF NOT EXISTS channels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(1000) NOT NULL,
                    logo_url VARCHAR(1000) NOT NULL
                    );
        """

        self.db.execute(sql)


    def insert(self, channel: CHANNEL):
        sql = f"""
            INSERT INTO channels (name, logo_url)
                    VALUES (%s, %s); 
            """

        self.db.execute(sql, params=(channel.name, channel.logoUrl,))
        row = self.db.execute("SELECT LAST_INSERT_ID() AS id", fetchone=True)

        if not row:
            return None

        channel.id = row["id"]

        return channel.id

    def get_by_name(self, channel: CHANNEL):
        sql = f"""
           SELECT id, name, logo_url from channels WHERE name = (%s);
        """

        row = self.db.execute(sql, params=(channel.name,), fetchall=True)

        if not row:
            return None
        return CHANNEL(id=row["id"], name=row["name"],logoUrl=row["logo_url"])

    def get_by_id(self, channel: CHANNEL):
        sql = f"""
           SELECT id, name, logo_url from channels WHERE id = (%s);
        """

        row = self.db.execute(sql, params=(channel.id,), fetchall=True)

        if not row:
            return None
        return CHANNEL(id=row["id"], name=row["name"],logoUrl=row["logo_url"])
    
    def delete(self, channel: CHANNEL):
        sql = f"""
        DELETE FROM channel
        WHERE id = (%s);
        """

        self.db.execute(sql, params=(channel.id,))

    def update(self, channel: CHANNEL):
        sql = f"""
        UPDATE channels
        SET logo_url = (%s) WHERE id = (%s);
        """

        self.db.execute(sql, params=(channel.logoUrl, channel.id,))
