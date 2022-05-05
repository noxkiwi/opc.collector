# RelayItem fields.
class OpcItem:
    OpcItemId = ""
    OpcItemCreated = ""
    OpcItemModified = ""
    OpcItemFlags = ""
    OpcItemAddress = ""
    GroupId = ""
    RemoteNode = None
    GroupItem = None
    LastValue = None

    def __init__(self, row):
        self.OpcItemId        = row[0]
        self.OpcItemCreated   = row[1]
        self.OpcItemModified  = row[2]
        self.OpcItemFlags     = row[3]
        self.OpcItemAddress   = row[4]
        self.GroupId          = row[5]
        self.LastValue        = row[6]

    def update():
        return None
