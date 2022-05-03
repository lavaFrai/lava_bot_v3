class ParsePing:
    def __init__(self, ping: str):
        self.id = int(ping[2:-1])
