from modules.Information.debuginfo import DebugInfo


class ModuleManager:
    def __init__(self):
        self.Modules = list()

        self.Modules.append(DebugInfo())

    def getModule(self, name: str):
        for i in self.Modules:
            if i.name == name:
                return i
        return None
