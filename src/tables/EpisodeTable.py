from classes.EPISODE import EPISODE
from tables.Database import Database
from utils.Date import Date


class EpisodeTable:
    def __init__(self, db: Database, tvshowName: str) -> None:
        self.db = db
        self.Date = Date()
        self.name = tvshowName
        self.createTable()

    def createTable(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.name} (
                    date DATE PRIMARY KEY, 
                    page_link VARCHAR(500) NULL,
                    link VARCHAR(500) NULL,
                    title VARCHAR(500) NULL,
                    type VARCHAR(100) NULL,
                    thumbnail VARCHAR(500) NULL
                    );
        """
        self.db.execute(sql)

    def batch_insert_all(self, episodes: list[EPISODE]) -> list[EPISODE] | None:
        """Insert all episodes in list"""
        index = 1
        batch = []
        for episode in episodes:
            index += 1
            # print(f"Adding episode {index}...")

            sql = f"""
                INSERT INTO {self.name} (date, page_link, link, title, type, thumbnail)
                VALUES (%s, %s, %s, %s, %s, %s);  
                """

            date = self.Date.convert_date_apnetv_to_mysql_format(episode.date)
            batch.append(
                (
                    date,
                    episode.pageUrl,
                    episode.contentUrl,
                    episode.title,
                    episode.contentType,
                    episode.thumbnail,
                )
            )
            # self.db.execute(sql, params=(date, episode.pageUrl, episode.contentUrl, episode.title, episode.contentType, episode.thumbnail,))

        sql = f"""
                INSERT INTO {self.name} (date, page_link, link, title, type, thumbnail)
                VALUES (%s, %s, %s, %s, %s, %s);  
                """

        self.db.execute(query=sql, params=batch, executemany=True)

        print("Added to the table")

        # return episodes

    def insert_all(self, episodes: list[EPISODE]) -> list[EPISODE] | None:
        """Insert all episodes in list"""
        index = 1
        for episode in episodes:
            print(f"Adding episode {index}...")

            sql = f"""
                INSERT INTO {self.name} (date, page_link, link, title, type, thumbnail)
                VALUES (%s, %s, %s, %s, %s, %s);  
                """

            date = self.Date.convert_date_apnetv_to_mysql_format(episode.date)
            self.db.execute(
                sql,
                params=(
                    date,
                    episode.pageUrl,
                    episode.contentUrl,
                    episode.title,
                    episode.contentType,
                    episode.thumbnail,
                ),
            )

            index += 1

        return episodes

    def insert(self, episode: EPISODE):
        sql = f"""
           INSERT INTO {self.name} (date, page_link, link, title, type, thumbnail)
                VALUES (%s, %s, %s, %s, %s, %s); 
        """

        date = self.Date.convert_date_apnetv_to_mysql_format(episode.date)

        self.db.execute(
            sql,
            params=(
                date,
                episode.pageUrl,
                episode.contentUrl,
                episode.title,
                episode.contentType,
                episode.thumbnail,
            ),
        )

    def oldest_episode(self) -> list[EPISODE]:
        sql = f"""
        SELECT * FROM {self.name} ORDER BY date LIMIT 1 OFFSET 0;
        """

        # Return top episode from table
        rows = self.db.execute(sql, params=None, fetchall=True)

        if not rows:
            return None

        episodes = []

        for row in rows:
            episode = EPISODE(
                date=row["date"],
                pageUrl=row["page_link"],
                thumbnail=row["thumbnail"],
                contentUrl=row["link"],
                contentType=row["type"],
                title=row["title"],
            )
            episodes.append(episode)

        return episodes

    def latest_episode(self) -> list[EPISODE]:
        sql = f"""
        SELECT * FROM {self.name} ORDER BY date desc LIMIT 1 OFFSET 0;
        """

        # Return top episode from table
        rows = self.db.execute(sql, params=None, fetchall=True)

        if not rows:
            return None

        episodes = []

        for row in rows:
            episode = EPISODE(
                date=row["date"],
                pageUrl=row["page_link"],
                thumbnail=row["thumbnail"],
                contentUrl=row["link"],
                contentType=row["type"],
                title=row["title"],
            )
            episodes.append(episode)

        return episodes

    def get_all(self, startNumber: int, endNumber: int) -> list[EPISODE]:
        """
        Retrieve a subset of data from the database based on specified range.

        Parameters:
        startNumber (int): The starting index (inclusive) for retrieving records.
        endNumber (int): The ending index (inclusive) for retrieving records.

        Returns:
        list[EPISODE] | None: A list of EPISODE data from the database, or None if no records are found.

        Notes:
        - The number of results to retrieve is calculated as End.
        - Records are skipped based on the Offset, defined as Start - 1.
        - If the result count is less than 0, it is adjusted to 0.
        """

        # limit = endNumber - startNumber + 1
        offset = startNumber - 1

        if offset < 0:
            offset = 0

        # sql = f"""
        #     SELECT * FROM (SELECT * FROM {self.name} ORDER BY date LIMIT {endNumber} OFFSET {offset}) as limited_dates ORDER BY date DESC;
        #
        # """
        sql = f"""
            SELECT * FROM {self.name} ORDER BY date desc LIMIT {endNumber} OFFSET {offset};  
        """

        rows = self.db.execute(sql, params=None, fetchall=True)

        try:
            episodes = []

            for row in rows:
                episode = EPISODE(
                    date=row["date"],
                    pageUrl=row["page_link"],
                    thumbnail=row["thumbnail"],
                    contentUrl=row["link"],
                    contentType=row["type"],
                    title=row["title"],
                )
                episodes.append(episode)
        except Exception as e:
            print(e)
            exit()

        return episodes

    def get_by_date(self, date: str):
        episode = EPISODE(date=date)

        sql = f"""
           SELECT date, page_link, link, title, type, thumbnail from {self.name} WHERE date = (%s);
        """

        row = self.db.execute(
            sql, params=(episode.convert_date_apnetv_to_mysql_format(),), fetchall=True
        )

        if not row:
            return None

        row = row[0]

        return EPISODE(
            date=row["date"],
            pageUrl=row["page_link"],
            thumbnail=row["thumbnail"],
            contentUrl=row["link"],
            contentType=row["type"],
            title=row["title"],
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
        SET page_link = %s,
            link = %s,
            title = %s,
            type = %s,
            thumbnail = %s
        WHERE date = %s;
        """

        self.db.execute(
            sql,
            params=(
                episode.pageUrl,
                episode.contentUrl,
                episode.title,
                episode.contentType,
                episode.thumbnail,
                episode.convert_date_apnetv_to_mysql_format(),
            ),
        )

    def batch_update_all(self, episodes: list[EPISODE]) -> list[EPISODE] | None:
        """Insert all episodes in list"""
        index = 1
        batch = []
        for episode in episodes:
            index += 1
            # print(f"Adding episode {index}...")
            date = self.Date.convert_date_apnetv_to_mysql_format(episode.date)

            batch.append(
                (
                    episode.pageUrl,
                    episode.contentUrl,
                    episode.title,
                    episode.contentType,
                    episode.thumbnail,
                    date,
                )
            )
            # self.db.execute(sql, params=(date, episode.pageUrl, episode.contentUrl, episode.title, episode.contentType, episode.thumbnail,))

        sql = f"""
                UPDATE {self.name}
                SET page_link = %s,
                    link = %s,
                    title = %s,
                    type = %s,
                    thumbnail = %s
                WHERE date = %s;
                """

        self.db.execute(query=sql, params=batch, executemany=True)

        print("Added to the table")
