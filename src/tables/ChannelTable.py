from classes.CHANNEL import CHANNEL
from tables.Database import Database


class ChannelTable:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.createTable()

    def createTable(self):
        """Create table if not existing"""
        sql = f"""
            CREATE TABLE IF NOT EXISTS channels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) UNIQUE NOT NULL,
                    logo_url VARCHAR(1000) NOT NULL,
                    page_url VARCHAR(1000) NOT NULL
                    );
        """

        self.db.execute(sql)

    def insert_all(self, channels: list[CHANNEL]) -> list[CHANNEL] | None:
        """Insert all channels in list"""
        index = 1
        for channel in channels:
            print(f"Adding channel {index}...")

            sql = f"""
                INSERT INTO channels (name, logo_url, page_url)
                        VALUES (%s, %s, %s); 
                """

            self.db.execute(
                sql,
                params=(
                    channel.name,
                    channel.logoUrl,
                    channel.pageUrl,
                ),
            )
            channel.id = index

            index += 1

        return channels

    def insert(self, channel: CHANNEL) -> CHANNEL | None:
        sql = f"""
            INSERT INTO channels (name, logo_url, page_url)
                    VALUES (%s, %s, %s); 
            """

        self.db.execute(
            sql,
            params=(
                channel.name,
                channel.logoUrl,
                channel.pageUrl,
            ),
        )
        row = self.db.execute("SELECT LAST_INSERT_ID() AS id", fetchone=True)

        if not row:
            return None

        channel.id = int(row["id"])

        return channel

    def get_all(self) -> CHANNEL:
        """Return all the data inside the database"""
        sql = """
            SELECT * FROM channels;
        """

        rows = self.db.execute(sql, params=None, fetchall=True)

        if not rows:
            return None

        channels = []

        for row in rows:
            channel = CHANNEL(
                id=row["id"],
                name=row["name"],
                logoUrl=row["logo_url"],
                pageUrl=row["page_url"],
            )
            channels.append(channel)

        return channels

    def get_by_name(self, name: str):
        sql = f"""
           SELECT id, name, logo_url, page_url from channels WHERE name = (%s);
        """

        row = self.db.execute(sql, params=(name,), fetchall=True)

        if not row:
            return None
        row = row[0]
        return CHANNEL(
            id=row["id"],
            name=row["name"],
            logoUrl=row["logo_url"],
            pageUrl=row["page_url"],
        )

    def get_by_id(self, channel: CHANNEL):
        sql = f"""
           SELECT id, name, logo_url, page_url from channels WHERE id = '(%s)';
        """

        row = self.db.execute(sql, params=(channel.id,), fetchall=True)

        if not row:
            return None
        row = row[0]
        return CHANNEL(
            id=row["id"],
            name=row["name"],
            logoUrl=row["logo_url"],
            pageUrl=row["page_url"],
        )

    def delete(self, channel: CHANNEL):
        """Delete Channel"""
        sql = f"""
        DELETE FROM channel
        WHERE id = (%s);
        """

        self.db.execute(sql, params=(channel.id,))

    def update(self, channel: CHANNEL):
        """Update the Channel Data"""
        sql = f"""
        UPDATE channels
        SET name = (%s), logo_url = (%s), page_url = (%s) WHERE id = (%s);
        """

        self.db.execute(
            sql,
            params=(
                channel.name,
                channel.logoUrl,
                channel.pageUrl,
                channel.id,
            ),
        )
