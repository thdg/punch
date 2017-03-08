import mysql.connector
from datetime import datetime
import pygame as pg
from random import random, randint
import time


def main():
    tags = ["female", "20_29"]

    wav_folder = "ogg/"
    db_name = "cocktail"
    
    with open("wav_info.txt", "r") as info:
        lines = info.readlines()
    
    cnx = mysql.connector.connect(user="root", 
        password="root", host="localhost", database=db_name)
    c = cnx.cursor()


    snippet_set_multiple = (
        "(SELECT name, sex, age "
        "from sounds s "
        "where sex = %s "
        "order by rand() "
        "limit %s) "
        "UNION "
        "(SELECT name, sex, age "
        "from sounds s "
        "where sex = %s "
        "order by rand() "
        "limit %s) "
        "order by age")
    
    nmale, nfemale = 5000, 5000
    c.execute(snippet_set_multiple, ("male", nmale, "female", nfemale))
    #c.execute(snippet_set, ("20_29", 100,))

    file_names = []
    for (name, sex, age) in c:
        file_names.append((name, sex, age))

    c.close()
    cnx.close()

    pg.mixer.init(frequency=16000)

    mixers = []
    for name, sex, age in file_names:
        mixers.append((pg.mixer.Sound(wav_folder + name), sex, age))

    pg.mixer.set_num_channels(1000)

    while len(mixers) > 0:
        delay = .01 + random() * .0010
        time.sleep(delay)
        c = pg.mixer.find_channel()
        i = randint(0, len(mixers)-1)
        i = 0
        s, sex, age = mixers.pop(i)
        if sex == "male":
            left, right = 1.0, 0.0
        else:
            left, right = 0.0, 1.0

        c.set_volume(left, right)
        c.play(s)
        print(len(mixers), sex, age)
    
    while pg.mixer.music.get_busy() == True:
        continue  # Finish all sounds

if __name__ == "__main__":
    main()

