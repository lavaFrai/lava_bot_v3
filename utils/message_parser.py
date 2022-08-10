from utils.event.OnMessageEventInfo import OnMessageEventInfo


class MessageParser:
    def __init__(self, ctx: OnMessageEventInfo):
        self.text = ctx.message.content
        self.ctx = ctx
        self.parsedContentRaw = self.ctx.message.content.split()
        self.parsedContent = []
        for i in self.parsedContentRaw:
            if i.strip() != "":
                self.parsedContent.append(i.strip())
        if self.parsedContent[0] == ctx.server_config.prefix or self.parsedContent[0] == f"<@{ctx.message.guild.me.id}>":
            self.parsedContent = self.parsedContent[2:]
        else:
            self.parsedContent = self.parsedContent[1:]
        self.parsedContentLower = list(map(lambda x: x.lower(), self.parsedContent))

    def __len__(self):
        return len(self.parsedContent)

    def __getitem__(self, item):
        return self.parsedContent[item]
