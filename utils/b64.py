import base64


def b64toBytes(text: str) -> str:
    return base64.b64encode(text.encode('utf8')).decode('utf8')


def b64fromBytes(text: str):
    return base64.b64decode(text.encode('utf8')).decode('utf8')
