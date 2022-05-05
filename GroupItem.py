# RelayItem fields.
class GroupItem:
    GroupId = ""
    GroupName = ""
    GroupType = ""
    GroupInterval = ""
    GroupTable = ""
    BaseClient = None
    ArchiveThread = None

    def __init__(self, row, archiveThread):
        self.ArchiveThread = archiveThread
        self.GroupId       = row[0]
        self.GroupName     = row[1]
        self.GroupType     = row[2]
        self.GroupInterval = row[3]
        self.GroupTable    = row[4]

    def update(self):
        return None
