from ItemValueCache import ItemValueCache
from noxLogger import noxLogger


# I am the internal RemoteSubscriptionHandler of the BaseServer
class RemoteSubscriptionHandler(object):

    # I will update the given node to the given value when changed.
    def datachange_notification(self, node, val, data):
        if val is None:
            noxLogger.error("0x00020021 value is None.")
            return None

        RemoteNode = ItemValueCache.GetRemoteNode(node)
        if RemoteNode is None:
            noxLogger.error("0x00020022 RemoteNode is None.")
            return None

        ItemValueCache.SetData(RemoteNode.OpcItemAddress, val)
        noxLogger.debug("0x00020023 " + RemoteNode.OpcItemAddress + " changed to " + str(val))

        if RemoteNode.GroupItem.GroupType != "E":
            noxLogger.debug("0x00020024 dataChanged: Not an event based value. Finished.")

        RemoteNode.GroupItem.ArchiveThread.subscriptionTriggered(RemoteNode.OpcItemAddress, val)
        noxLogger.debug("0x00020025 " + RemoteNode.OpcItemAddress + " was changed successfully.")

    def event_notification(self, event):
        return None
