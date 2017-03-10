import time
from random import random, randint

import mysql.connector

import pygame as pg


def play(left, right, delay=.1, delay_v=.01, gain=1, gain_v=0, repeat=False, shuffle=False):

    lset, rset = set(left), set(right)

    mixers = left + right
    try:
        while repeat or len(mixers) > 0:
            d = delay + random() * delay_v
            g = gain + random() * gain_v
            time.sleep(d)
            c = pg.mixer.find_channel()
            i = randint(0, len(mixers) - 1) if shuffle else 0
            s = mixers.pop(i) if not repeat else mixers[i]
            if s in lset:
                left, right = g, 0.0
            else:
                left, right = 0.0, g

            c.set_volume(left, right)
            c.play(s)
            print(len(mixers))
    except KeyboardInterrupt:
        pass  # Stop playing

    while pg.mixer.music.get_busy():
        pass  # Loop until all sounds have finished playing


def main(m, f):
    sounds_folder = "ogg/"
    db_name = "cocktail"

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
        "order by sex, age")
    
    nmale, nfemale = m, f
    c.execute(snippet_set_multiple, ("male", nmale, "female", nfemale))

    snippets = []
    for (name, sex, age) in c:
        snippets.append((name, sex, age))

    c.close()
    cnx.close()

    frequency = 16000
    channels = 1000
    pg.mixer.init(frequency=frequency)
    pg.mixer.set_num_channels(channels)

    mixers = []
    for name, sex, age in snippets:
        mixers.append(pg.mixer.Sound(sounds_folder + name))

    play(mixers[:nfemale], mixers[nfemale:], shuffle=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Play clusters.')
    parser.add_argument('male', type=int)
    parser.add_argument('female', type=int)

    args = parser.parse_args()
    main(args.male, args.female)

