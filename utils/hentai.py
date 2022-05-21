import json
import random

import hmtai


class HentaiGenerator:
    def __init__(self):
        self.possible = hmtai.listHM("2")
        self.possible = self.possible[self.possible.index('['):
                                      self.possible.rindex(']') + 1].replace('\'', '"')
        self.possible = json.JSONDecoder().decode(self.possible)

    def GetRandomUrl(self, tag=None):
        if tag is None or tag not in self.possible:
            return hmtai.useHM("2", random.choice(self.possible))
        return hmtai.useHM("2", tag)

