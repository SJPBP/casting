import re

input_string = "position:relative;background-image:url('https://apnetv.xyz/db_imgs/serial_Taarak-Meh_1702877246.jpg?xyz');"


print(re.findall("'([^']*)'", input_string))

