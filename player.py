import pygame as pg


class Player(object):

    def __init__(self, frequency=16000, channels=100):
        self.frequency = frequency
        self.channels = channels

        pg.mixer.init(frequency=frequency)
        pg.mixer.set_num_channels(channels)

    def fire(self, path, volume=(1, 1)):
        s = pg.mixer.Sound(path)
        c = pg.mixer.find_channel()
        if c is not None:
            c.set_volume(*volume)
            c.play(s)
