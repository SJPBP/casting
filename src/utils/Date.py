from datetime import datetime
import re

class Date:
    def __init__(self) -> None:
        pass

    def is_date_obj(self, date) -> bool:
        """
        Check if the provided argument is a `date` object.

        Returns:
        bool: True if the argument is a `date` object; otherwise, False.
        """
        if date is datetime.date:
            return True
        else:
                return False

        
    def ordinal(self, n: int):
        """Add th, st, dn, rd to numercal dates"""
        return str(n) + ("th" if 4 <= n % 100 <=20 else { 1:"st", 2:"nd", 3:"rd"}.get(n%10, "th"))
    
    def convert_date_apnetv_to_mysql_format(self, date) -> str:
        """Returns string date in format used in mysql db"""
        mysql_format = "%Y-%m-%d"

        # Check if date is datetime object
        if not self.is_date_obj(date):
            date = str(date)
            
            # Convert string to datetime object in mysql_format
            date = self.convert_date_from_apnetv_format_to_desired(date, mysql_format)

            return date        

        # return self.date_in_apnetv_format(mysql_format)
        
    def convert_date_from_mysql_to_apnetv_format(self, date) -> str:
        """
        Convert date from mysql into format usin in ApneTV
        """
        # Format used in apnetv
        apneTV_format = "%d %B %Y"
        mysql_format = "%Y-%m-%d"
        date = str(date)
        
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

    def convert_date_from_apnetv_to_datetime(self, date):
        try:
            # Get the date
            date = date.replace("Februay", "February")

            # 1. Trim whitespace
            date_str = date.strip()

            # 2. Remove ordinal suffixes (st, nd, rd, th)
            date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

            # 3. Parse safely
            return datetime.strptime(date_str, "%d %B %Y")

        except Exception as e:
            print(e)
            return False
    
    def convert_date_from_apnetv_format_to_desired(self, date, fmt: str) -> str | bool:
        try:
            # Get the date
            date = date.replace("Februay", "February")

            # 1. Trim whitespace
            date_str = date.strip()

            # 2. Remove ordinal suffixes (st, nd, rd, th)
            date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

            # 3. Parse safely
            formatedDate = datetime.strptime(date_str, "%d %B %Y")
            dt = formatedDate.strftime(fmt)

            return dt
        except Exception as e:
            print(e)
            return False
