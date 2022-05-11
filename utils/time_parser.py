import re
from datetime import timedelta


def str_to_delta(s):
    import re
    from datetime import timedelta
    reg = re.compile(r'(\d+)d|(\d+)s|(\d+)µs|(\d+)ms|(\d+)m|(\d+)h|(\d+)w')
    params = [sum(int(e) for e in t if e) for t in zip(*reg.findall(s))]
    return timedelta(*params)


class ParseTime:
    def __init__(self, time: str):
        self.time = str_to_delta(time)
