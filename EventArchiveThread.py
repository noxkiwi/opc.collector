from datetime import datetime

from ArchiveThread import ArchiveThread
from DatabaseManager import DatabaseManager
from GroupItem import GroupItem
from noxLogger import noxLogger


class EventArchiveThread(ArchiveThread):
    BaseClient = None
    scanEnable = None

    def __init__(self, group_row, base_client):
        super().__init__(group_row, base_client)
        self.GroupItem = GroupItem(group_row, self)
        noxLogger.debug("0x00030211 Create ArchiveThread for group " + self.GroupItem.GroupName)
        self.BaseClient = base_client
        self.Subscription = self.BaseClient.create_subscription(500, self.SubscriptionHandler)
        noxLogger.debug("0x00030012 Created ArchiveThread for group " + self.GroupItem.GroupName)
        self.scanEnable = False
        self.DatabaseManager = DatabaseManager()

    # I am triggered from the subscription and tell the ArchiveThread to "Now create an entry!"
    def subscriptionTriggered(self, field, value):
        noxLogger.debug("0x00031021 " + field + " subscription triggered.")
        self.Field = field
        self.Value = value
        self.saveEntry()

    # I will save the current entry.
    def saveEntry(self):
        queryString = "INSERT INTO `" + self.GroupItem.GroupTable + "` (`" + self.GroupItem.GroupTable + "_created`, `" + self.Field + "`) VALUES (CURRENT_TIMESTAMP, " + str(
            self.Value) + ");"
        queryData = (1, 2, 3)

        self.DatabaseManager.query(queryString, queryData)
        noxLogger.debug("0x00031011 Database query " + queryString + " successful.")
        self.Field = None
        self.Value = None
        return True
