import time


class Logger:
    LOG_LEVEL_DEBUG = 0
    LOG_LEVEL_LOG = 1
    LOG_LEVEL_WARNING = 2
    LOG_LEVEL_ERROR = 3

    def __init__(self, log_level: int = LOG_LEVEL_LOG, file: open = None):
        self.file = file
        self.log_level = log_level

    def printText(self, text):
        if self.file is None:
            print(text)
        else:
            self.file.write(text + '\n')

    def Log(self, text):
        if self.log_level <= self.LOG_LEVEL_LOG:
            self.printText(f"{time.strftime('%a, %d %b %Y %H:%M:%S UTC%z')} [INFO]\t\t" + text)

    def Debug(self, text):
        if self.log_level <= self.LOG_LEVEL_DEBUG:
            self.printText(f"{time.strftime('%a, %d %b %Y %H:%M:%S UTC%z')} [DEBUG]\t\t" + text)

    def Warning(self, text):
        if self.log_level <= self.LOG_LEVEL_WARNING:
            self.printText(f"{time.strftime('%a, %d %b %Y %H:%M:%S UTC%z')} [WARNING]\t\t" + text)

    def Error(self, text):
        if self.log_level <= self.LOG_LEVEL_ERROR:
            self.printText(f"{time.strftime('%a, %d %b %Y %H:%M:%S UTC%z')} [ERROR]\t\t" + text)
        exit(-1)
