from BaseClient import BaseClient


class ServerItem:
    ServerId = None
    ServerCreated = None
    ServerModified = None
    ServerFlags = None
    ServerAddress = None
    ServerPort = None
    ServerEndpoint = None
    OpcClient: BaseClient = None

    def __init__(self, row):
        self.ServerId = row[0]
        self.ServerCreated = row[1]
        self.ServerModified = row[2]
        self.ServerFlags = row[3]
        self.ServerAddress = row[4]
        self.ServerPort = row[5]
        self.ServerEndpoint = row[6]

    def update():
        return None
