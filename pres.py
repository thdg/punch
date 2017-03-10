import time
from random import random, randint

import pygame as pg


def play(left, right, delay=.1, delay_v=.05, gain=1, gain_v=0, repeat=False, shuffle=False):
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
            c.play(s, maxtime=1000)
    except KeyboardInterrupt:
        pass  # Stop playing

    while pg.mixer.music.get_busy():
        pass  # Loop until all sounds have finished playing


def main(l, r):
    sounds_folder = "ogg/"

    frequency = 16000
    channels = 1000
    pg.mixer.init(frequency=frequency)
    pg.mixer.set_num_channels(channels)

    with open("left.txt") as f:
        left_files = f.readlines()

    with open("right.txt") as f:
        right_files = f.readlines()

    lmixers, rmixers = [], []
    for name in left_files:
        lmixers.append(pg.mixer.Sound(sounds_folder + name.strip()))
    for name in right_files:
        rmixers.append(pg.mixer.Sound(sounds_folder + name.strip()))

    play(lmixers if l else [], rmixers if r else [], shuffle=True, repeat=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Play clusters.')
    parser.add_argument('-l', dest='l', action='store_true')
    parser.add_argument('-r', dest='r', action='store_true')

    args = parser.parse_args()
    main(args.l, args.r)

