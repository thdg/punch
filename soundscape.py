import random

from player import Player

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.animation import FuncAnimation


def dist(a, b):
    values = []
    for _a, _b in zip(a, b):
        if _a is not None and _b is not None:
            values.append(abs(_a-_b))

    if len(values) > 0:
        return sum(values)/len(values)

    return 0


def set_list(lines, row):
    return sorted(list(set(line[row] for line in lines)))


def choice(l, normalize=True):
    def _choice(v):
        try:
            return l.index(v)/(len(l)-1 if normalize else 1)
        except ValueError:
            return -1

    return _choice


class SoundScape(object):
    def __init__(self, data):
        self.data = data
        self.pos = []
        self.vectors = []
        self.active = set()
        self.closest = None

        self.pickup_range = data.get("pickup_range", 0.2)

        self.sliders = []
        self.radios = []

        self.fig = plt.figure(figsize=(10, 4))

        with open(data["info_file"]) as f:
            lines = [line.split(data["delimiter"]) for line in f.readlines()]

        self.mappings = []
        for i, dim in enumerate(data["dimensions"]):
            t = dim["type"]
            row = dim["row"]
            self.pos.append(dim.get("default", 0))

            if t == "radio":
                c = dim.get("choices", set_list(lines, row))
                print(c)
                self.mappings.append(choice(c))
                wpos = [len(self.radios)*.16, 0.5, 0.15, .5]
                ax = plt.axes(wpos)
                radio = RadioButtons(ax, c, active=0)
                radio.on_clicked(self.update_function(i))
                self.radios.append(radio)
            elif t == "float":
                self.mappings.append(float)
                wpos = [.2, len(self.sliders)*.10, .5, .1]
                ax = plt.axes(wpos)
                slider = Slider(ax, dim["name"], 0, 1, valinit=0)
                slider.on_changed(self.update_function(i))
                self.sliders.append(slider)
            elif t == "len":
                self.mappings.append(len)
                wpos = [.2, len(self.sliders)*.10, .5, .1]
                ax = plt.axes(wpos)
                slider = Slider(ax, dim, 0, 1, valinit=0)
                slider.on_changed(self.update_function(i))
                self.sliders.append(slider)

        for line in lines:
            dim_values = []
            for i, dim in enumerate(data["dimensions"]):
                dim_values.append(self.mappings[i](line[dim["row"]]))
            self.vectors.append((
                data["root_folder"] + line[data["path_row"]],
                *dim_values
            ))

        self.update_position()

    def update_function(self, i):
        def _update(v):
            self.pos[i] = self.mappings[i](v)
            self.update_position()

        return _update

    def update_position(self):
        self.active = set()
        closest = None
        for path, *v in self.vectors:
            d = dist(self.pos, v)
            if d < self.pickup_range:
                self.active.add((path, d, *v))
            if closest is None or closest[1] > d:
                closest = (path, d, *v)
        self.closest = closest

    def volume(self, d):
        l = 1 - d*(1/self.pickup_range)
        return l, l

    def play(self):

        player = Player()

        pickup_range = self.data["pickup_range"]
        delay = self.data.get("delay", 10)

        def update(t):
            if len(self.active) > 0:
                path, d, *v = random.sample(self.active, 1)[0]
                player.fire(path, volume=self.volume(d))

        animation = FuncAnimation(self.fig, update, interval=delay)
        plt.show()

