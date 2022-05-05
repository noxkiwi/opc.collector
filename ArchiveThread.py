from BaseItem import BaseItem
from OpcItem import OpcItem
from RemoteSubscriptionHandler import RemoteSubscriptionHandler
# I am an arbitrary ArchiveThread. My purpose is to store data into sqlite whenever I am triggered.
# My trigger may be based on intervals or events.
from noxLogger import noxLogger
from GroupItem import GroupItem
from DatabaseManager import DatabaseManager


class ArchiveThread:
    # I am the DatabaseManager.
    # TODO: Make this available through the Server, instead of opening multiple connections here!
    DatabaseManager = None
    # I am the base client
    # TODO: Make this available through the Server, instead of opening multiple connections here!
    BaseClient = None
    # I am the groupItem instance for this ArchiveThread.
    GroupItem = None
    # I am the Sub itself
    Subscription = None
    # I am opcItem instances created in the Thread to include in the ArchiveThread to store data.
    OpcItems = []
    # I am the list of subscriptions
    Subscriptions = {}
    # I am the time of THE entry created.
    EntryTime = None
    # I am the trigger for the thread!
    ScanEnable = False
    # I am the scanner thread for this archiveThread
    ScanThread = None
    # I am the Sub Handler
    SubscriptionHandler = RemoteSubscriptionHandler()
    # I am the Field
    Field = None
    # I am the value of the field
    Value = None

    # Constructor.
    def __init__(self, group_row, base_client):
        self.BaseClient = base_client
        self.GroupItem = GroupItem(group_row, self)
        noxLogger.debug("0x00030011 Create ArchiveThread for group " + self.GroupItem.GroupName)
        self.Subscription = self.BaseClient.create_subscription(500, self.SubscriptionHandler)
        noxLogger.debug("0x00030012 Created ArchiveThread for group " + self.GroupItem.GroupName)
        self.Field = None
        self.Value = None

    # I will add the given opcItem to the Thread.
    def AddOpcItem(self, myOpcItem: OpcItem):
        try:
            self.OpcItems.append(myOpcItem)
            noxLogger.debug("0x00030021 " + myOpcItem.OpcItemAddress + " added to group " + self.GroupItem.GroupName)
        except:
            noxLogger.error(
                "0x00030022 " + myOpcItem.OpcItemAddress + " not added to group " + self.GroupItem.GroupName)
            return None
        try:
            self.Subscription.subscribe_data_change(myOpcItem.RemoteNode)
            noxLogger.debug(
                "0x00030023 " + myOpcItem.OpcItemAddress + " subscribed at group " + self.GroupItem.GroupName)
        except Exception as ex:
            noxLogger.error(myOpcItem.LastValue)
            noxLogger.error(myOpcItem.OpcItemAddress)
            print(ex)
            noxLogger.error(
                "0x00030024 " + myOpcItem.OpcItemAddress + " not subscribed at group " + self.GroupItem.GroupName)

    # I will set the given field to the given value for the next saveEntry call.
    def setField(field, value):
        return None

    def scan_on(self):
        # self.scan_thread.setDaemon(True)
        self.ScanEnable = True

    def scan_off(self):
        # self.scan_thread.setDaemon(False)
        self.ScanEnable = False

    # I am triggered from the subscription and tell the ArchiveThread to "Now create an entry!"
    def subscriptionTriggered(self, field, value):
        return None

    # I will save the current entry.
    def saveEntry(self):
        return None
