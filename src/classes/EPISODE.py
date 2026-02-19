from dataclasses import dataclass
from datetime import datetime


@dataclass
class EPISODE:
    date: str
    pageUrl: str | None = None
    thumbnail: str | None = None
    contentUrl: str | None = None
    title: str | None = None
    contentType: str | None = None

    @property
    def json(self):
        """
        Return data in json
        """
        return {
            "Date": self.date,
            "Thumbnail": self.thumbnail,
            "ContentUrl": self.contentUrl,
            "ContentType": self.contentType,
            "Title": self.title,
            "PageUrl": self.pageUrl,
        }

    def update_content_type(self) -> str:
        """
        Return video extension of content url
        """
        if self.contentUrl:
            self.contentType = self.contentUrl.split(".")[-1]
            return self.contentType

    def add_date_to_title(self):
        """
        Add date to title and save it
        """
        if self.date is not None and self.title is not None:
            self.title = self.title + " " + self.date

    def is_date_obj(self) -> bool:
        """
        Check if the provided argument is a `date` object.

        Returns:
        bool: True if the argument is a `date` object; otherwise, False.
        """
        if self.date is datetime.date:
            return True
        else:
            return False

    def ordinal(self, n: int):
        """Add th, st, dn, rd to numercal dates"""
        return str(n) + (
            "th"
            if 4 <= n % 100 <= 20
            else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        )

    def convert_date_apnetv_to_mysql_format(self) -> str:
        """Returns string date in format used in mysql db"""
        mysql_format = "%Y-%m-%d"

        # Check if date is datetime object
        if not self.is_date_obj():
            date = str(self.date)

            # Convert string to datetime object in mysql_format
            date = self.convert_date_from_apnetv_format_to_desired(mysql_format)

            return date

        # return self.date_in_apnetv_format(mysql_format)

    def convert_date_from_mysql_to_apnetv_format(self) -> str:
        """
        Convert date from mysql into format usin in ApneTV
        """
        # Format used in apnetv
        apneTV_format = "%d %B %Y"
        mysql_format = "%Y-%m-%d"
        date = str(self.date)

        if self.date_in_format(date, apneTV_format):
            return date
        else:
            # This means date in mysql format
            # convert into datetime obj using it
            date = datetime.strptime(date, mysql_format)

            # Convert date into apnetv format
            date = datetime.strftime(date, apneTV_format)

            # Convert date back to string
            date = str(date)

        # Format the date into apne tv format then spilt by space
        day, month, year = date.split()

        # Add th to date numbers
        f_day = self.ordinal(int(day))

        # Connect them back
        formated_date = f"{f_day} {month} {year}"

        return formated_date

    def date_in_format(self, date, fmt: str) -> bool:
        """
        Check if the date matches the specified format.

        Parameters:
        fmt (str): The format against which the date will be validated.

        Returns:
        bool: True if the date conforms to the specified format; otherwise, False.
        """
        # Raise error if date not in given format
        try:
            date = str(date)
            datetime.strptime(date, fmt)
            return True
        except ValueError:
            return False

    def convert_date_from_apnetv_format_to_desired(self, fmt: str) -> str | bool:
        try:
            date = self.date
            # Get the date
            day = date.split()[0][-2:]

            if day == "th":
                formatedDate = datetime.strptime(date, "%dth %B %Y")
                dt = formatedDate.strftime(fmt)
            elif day == "rd":
                formatedDate = datetime.strptime(date, "%drd %B %Y")
                dt = formatedDate.strftime(fmt)
            elif day == "nd":
                formatedDate = datetime.strptime(date, "%dnd %B %Y")
                dt = formatedDate.strftime(fmt)
            elif day == "st":
                formatedDate = datetime.strptime(date, "%dst %B %Y")
                dt = formatedDate.strftime(fmt)
            else:
                raise Exception("Unkown date given")
            return dt
        except ValueError:
            return False
