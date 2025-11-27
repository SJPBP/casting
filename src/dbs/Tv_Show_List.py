from DB import DB
from mysql.connector import Error

class Tv_Show_List(DB):
    def __init__(self, channel_name:str) -> None:
        super().__init__()
        self.table_name: str = channel_name

        self.create_table()
    
    def create_table(self):
        # try:
            with super().connect_to_server() as conn:
                cursor = conn.cursor()
                query: str = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    tv_show_id VARCHAR(768) PRIMARY KEY NOT NULL,
                    tv_show_name VARCHAR(10000) NOT NULL, 
                    tv_show_thumbnail VARCHAR(10000) NOT NULL
                    total VARCHAR(10000) NOT NULL
                    );"""

                print("Connecting to channel table...", end="\n")
        
                print(query)

                cursor.execute(query)

                print("Succeed!")

                cursor.close()


        # except Error as e:
            # print("Failed!")
            # print(e)
        
    def add(self, channel_shows):
        try:
            with super().connect_to_server() as conn:
                cursor = conn.cursor()

                query = f"""INSERT INTO {self.table_name} (tv_show_id, tv_show_name, tv_show_thumbnail)
                    VALUES (%s, %s);
                    """

                # if "channel_name" in channel_shows and "channel_logo" in channel_shows:
                #     channel_name = channel_list['channel_name']
                #     channel_logo = channel_list['channel_logo']
                #


                tv_show_id: str = channel_shows["id"]
                tv_show_name: str = channel_shows["name"]
                tv_show_thumbnail: str = channel_shows["thumbnail"]

                print("Adding Channel TV Shows ID, Name And Thumbnail...", end="")

                cursor.execute(query, params=(tv_show_id, tv_show_name,tv_show_thumbnail,))
                conn.commit()

                print("Successed!")

                cursor.close()
                # else:
                #     cursor.close()
                #     raise Exception("Invaild Keys")

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

                print("Getting Channels ID, Name and Thumbnail...", end="")

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
    ch = Tv_Show_List("Colors")
    # ch_1 = {
    #     'channel_name': 'Sony-TV',
    #     'channel_logo': 'ApneTV_main_page_files/channel_Sony-TV_1702874645.png'
    # }

    ch.add(ch)

    # data: list = ch.get()[0]
    # print("Channels Name and Logo")
    # print(f"Name: {data[0]}")
    # print(f"Logo: {data[1]}")
