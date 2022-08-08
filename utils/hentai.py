import json
import random

import hmtai


class HentaiGenerator:
    def __init__(self):
        self.possible = ["anal", "ass", "bdsm", "cum", "classic", "creampie", "manga", "femdom", "incest", "masturbation",
                         "public", "ero", "orgy", "elves", "yuri", "pantsu", "glasses", "cuckold", "blowjob", "boobjob",
                         "boobs", "thighs", "pussy", "ahegao", "uniform", "gangbang", "tentacles", "nsfwNeko", "nsfwMobileWallpaper",
                         "foxgirl", "neko", "cry", "kiss", "waifu"]

    def GetRandomUrl(self, tag=None):
        if tag is None or tag not in self.possible:
            return hmtai.useHM("2", "hentai")
        try:
            return hmtai.useHM("2", tag)
        except hmtai.CategoryNotFound:
            return "https://iris-tg.ru/images/tg/items/134541.jpg"
