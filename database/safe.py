import sqlite3
import base64
import imageio
import cv2


PASSWORD = "1234"

connect = input("what is your password?\n")

while connect != PASSWORD:
    connect = input("what is your password")
    if connect == "q":
        break

if connect == PASSWORD:
    conn = sqlite3.connect('mysafe.db')
    try:
        conn.execute('''CREATE TABLE SAFE
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        print("your safe has been created!\nWhat would you like to store?")
    except:
        print("You have a safe, what would you like to do today?")

    while True:
        print("\n" + "*"*15)
        print("Command:")
        print("q = quit program")
        print("o = open file")
        print("s = store file")
        print("*"*15)
        input_ = input(":")

        if input_ == "q":
            break
        if input_ == "o":
            # oprn file
            file_type = input("what type of file you wanna open?\n")
            file_name = input(
                "what is name of your file you wanna open?\n")
            FILE_ = file_name + "." + file_type

            cursor = conn.execute(
                "SELECT * from SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"')

            file_string = ""
            for row in cursor:
                file_string = row[3]
            with open(FILE_, 'wb') as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string))

        if input_ == "s":
            # store file
            PATH = input("/Users/PREDATOR/Desktop/python_3project/database")

            FILE_TYPES = {
                "txt": "TEXT",
                "java": "TEXT",
                "dart": "TEXT",
                "py": "TEXT",
                "jpg": "IMAGE",
                "png": "IMAGE",
                "jpeg": "IMAGE"
            }

            file_name = PATH.split("/")
            file_name = file_name[len(file_name) - 1]
            file_string = ""

            NAME = file_name.split(".")[0]
            EXTENSION = file_name.split(".")[1]

            try:
                EXTENSION = FILE_TYPES[EXTENSION]
            except:
                Exception()

            if EXTENSION == "IMAGE":
                IMAGE = cv2.imread(PATH)
                file_string = base64.b64encode(
                    cv2.imencode('.jpg', IMAGE)[1]).decode()

            elif EXTENSION == "TEXT":
                file_string = open(PATH, "r").read()
                file_string = base64.b64encode(file_string)

            EXTENSION = file_name.split(".")[1]

            command = 'INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' % (
                '"' + file_name + '"', '"' + NAME + '"', '"' + EXTENSION + '"', '"' + file_string + '"')

            conn.execute(command)
            conn.commit()
