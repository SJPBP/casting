from DB import DB
from mysql.connector import Error

class Channel_List(DB):
    def __init__(self) -> None:
        super().__init__()
        self.table_name: str = "channel_list"

        self.create_table()
    
    def create_table(self):
        try:
            with super().connect_to_server() as conn:
                cursor = conn.cursor()
                query: str = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    channel_name VARCHAR(768) PRIMARY KEY,
                    channel_logo VARCHAR(10000)
                    );"""

                print("Connecting to channel list table...", end="")
        
                # super().execute(query)
                cursor.execute(query)

                print("Succeed!")

                cursor.close()


        except Error as e:
            print("Failed!")
            print(e)
        
    def add(self, channel_list):
        try:
            with super().connect_to_server() as conn:
                cursor = conn.cursor()

                query = f"""INSERT INTO {self.table_name} (channel_name, channel_logo)
                    VALUES (%s, %s);
                    """

                if "channel_name" in channel_list and "channel_logo" in channel_list:
                    channel_name = channel_list['channel_name']
                    channel_logo = channel_list['channel_logo']


                    print("Adding Channel Name And Logo...", end="")

                    cursor.execute(query, params=(channel_name, channel_logo,))
                    conn.commit()

                    print("Successed!")

                    cursor.close()
                else:
                    cursor.close()
                    raise Exception("Invaild Keys")

        except Exception as e:
            print("Failed!")
            print(e)

    def get(self):
        data = []
        try:
            with super().connect_to_server() as conn:
                cursor = conn.cursor()

                query = f"""
                    SELECT * FROM {self.table_name};
                    """

                print("Getting Channels Name and Logo...", end="")

                cursor.execute(query)

                data = cursor.fetchall()

                print("Succeed!")

                cursor.close()

                return data

        except Exception as e:
            print("Failed!")
            print(e)
            return data


if __name__ == "__main__":
    ch = Channel_List()
    ch_1 = {
        'channel_name': 'Sony-TV',
        'channel_logo': 'ApneTV_main_page_files/channel_Sony-TV_1702874645.png'
    }

    ch.add(ch_1)

    data: list = ch.get()[0]
    print("Channels Name and Logo")
    print(f"Name: {data[0]}")
    print(f"Logo: {data[1]}")
