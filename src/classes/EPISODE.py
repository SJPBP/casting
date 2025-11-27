from dataclasses import dataclass
from datetime import datetime

@dataclass
class EPISODE:
    date: str 
    thumbnail: str 
    contentUrl: str 
    title: str | None
    contentType: str | None = None

    def update_content_type(self) -> str:
        if self.contentUrl:
            self.contentType = self.contentUrl.split(".")[-1]
            return self.contentType
    
    def ordinal(self, n: int):
        """Add th, st, dn, rd to numercal dates"""
        return str(n) + ("th" if 4 <= n % 100 <=20 else { 1:"st", 2:"nd", 3:"rd"}.get(n%10, "th"))
    
    def get_date_in_mysql_format(self) -> str | bool:
        """Returns string date in format used in mysql db"""
        mysql_format = "%d-%m-%Y"
        
        if self.date_in_mysql_format(mysql_format):
            return self.date

        return self.date_in_apnetv_format(mysql_format)
        
    def get_date_in_apnetv_format(self) -> str:
        """Returns string date in format used in ApneTv Website"""
        apneTV_format = "%d %B %Y"
        
        if not self.date_in_apnetv_format(apneTV_format) is str:
            return self.date

        # Format the date into apne tv format then spilt by space
        day, month, year = self.date.split()

        # Add th to date numbers
        f_day = self.ordinal(int(day))

        # Connect them back
        formated_date = f"{f_day} {month} {year}"

        return formated_date
    
    def date_in_mysql_format(self, fmt: str) -> bool:
        try:
            datetime.strptime(self.date, fmt)
            return True
        except ValueError:
            return False
    
    def date_in_apnetv_format(self, fmt: str) -> str | bool:
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
