import os
import sys

from BaseClient import BaseClient
from EventArchiveThread import EventArchiveThread
from GroupItem import GroupItem
from IntervalArchiveThread import IntervalArchiveThread
from ItemValueCache import ItemValueCache
from OpcItem import OpcItem
from DatabaseManager import DatabaseManager
# I am the collector service.
from noxLogger import noxLogger


class CollectorService:
    # I am the OPC Server instance
    Server = None
    # I am the OPC Server namespace
    ServerNamespace = None
    # I am the OPC Server's root node
    root = None
    # I am the OPC Item tree
    tree = {}
    # I am the list of Items.
    Items = {}
    # I am the scanner thread.
    scanThread = None
    # I am the base client
    baseClient = None
    # I am the DM
    databaseManager = None

    def __init__(self):
        noxLogger.debug("0x00000011 Database connected")
        self.databaseManager = DatabaseManager()
        self.baseClient = BaseClient("opc.tcp://vulpes.home:4911/nox/base")
   #     self.baseClient.initialize()
        self.baseClient.connect()
        noxLogger.debug("0x00000011 opc.base connected")
        self.Connect()
        noxLogger.debug("0x00000012 Service online")


    # Connect to all groups.
    def Connect(self):
        queryString = """
SELECT
	`archive_group_id`,
	`archive_group_name`,
	`archive_group_type`,
	`archive_group_interval`,
	`archive_group_table`
FROM
	`archive_group`
WHERE TRUE
	AND `archive_group_flags` &1=1
;        """;
        queryData = (1,2,3)
        groupCursor = self.databaseManager.read(queryString, queryData)
        for groupRow in groupCursor:
            if groupRow[2] == "I":
                myThread = IntervalArchiveThread(groupRow, self.baseClient)
            if groupRow[2] == "E":
                myThread = EventArchiveThread(groupRow, self.baseClient)
            self.ConnectThread(myThread)
            myThread.scan_on()

    # I will return the array of nodes to the given address.
    def makeNodePath(self, address):
        branches = address.split(".")
        ret = []
        ret.append("0:Objects")
        for branch in branches:
            ret.append("2:" + branch)
        return ret

    # Connect a group and handle the rest
    def ConnectThread(self, myThread):
        queryString = """
SELECT
	`opc_item`.`opc_item_id`,
	`opc_item`.`opc_item_created`,
	`opc_item`.`opc_item_modified`,
	`opc_item`.`opc_item_flags`,
	`opc_item`.`opc_item_address`,
	`archive_item`.`archive_group_id`,
	`opc_item`.`opc_item_lastvalue`
FROM
    `archive_item`
    JOIN    `archive_group` USING (`archive_group_id`)
    JOIN    `opc_item`      USING (`opc_item_id`)
WHERE TRUE
    AND `archive_item`.`archive_item_flags`   &1=1
    AND	`opc_item`.`opc_item_flags`           &1=1
    AND	`archive_group`.`archive_group_flags` &1=1
    AND	`archive_group`.`archive_group_id`    =
        """;
        queryString = queryString + (str(myThread.GroupItem.GroupId))
        queryData = (1,2,3)
        opcItemCursor = self.databaseManager.read(queryString, queryData)

        for opcItemRow in opcItemCursor:
            myOpcItem           = OpcItem(opcItemRow)
            myOpcItem.GroupItem = myThread.GroupItem
            #self.databaseManager.query("CALL `prepareColumn`('lightsystem', '" + myOpcItem.GroupItem.GroupTable + "', '" + myOpcItem.OpcItemAddress + "', 'FLOAT(15,5)');",[])
            try:
                myOpcItem.RemoteNode = self.baseClient.get_server_node().get_child(self.makeNodePath(myOpcItem.OpcItemAddress))
                noxLogger.debug("0x00010011 " + myOpcItem.OpcItemAddress + " connected")
            except:
                noxLogger.error("0x00010012 " + myOpcItem.OpcItemAddress + " not connected")
                continue

            try:
                ItemValueCache.AddRemoteNode(myOpcItem)
                noxLogger.debug("0x00010013 " + myOpcItem.OpcItemAddress + " successfully added to IVC")
            except:
                noxLogger.error("0x00010014 " + myOpcItem.OpcItemAddress + " could not be added to IVC")
                continue

            try:
                myThread.AddOpcItem(myOpcItem)
                noxLogger.debug("0x00010015 " + myOpcItem.OpcItemAddress + " successfully added to archive thread")
            except:
                noxLogger.error("0x00010015 " + myOpcItem.OpcItemAddress + " not added to archive thread")
                continue

    # DEFAULT STUFF BEHIND THIS LINE!!!!

    def MakeNodePath(self, address):
        branches = address.split(".")
        ret = []
        ret.append("0:Objects")
        for branch in branches:
            ret.append("2:" + branch)
        return ret


    # Starts the scanner Thread.
    def ScanOn(self):
        self.scanThread = threading.Thread(target=self.doScan)
        self.scanEnable = True
        self.scanThread.start()
        return None

    # Stops the scanner thread.
    def ScanOff(self):
        self.scanEnable = False
        self.scanThread.join()
        return None

    # Generate Tree Branches and the end node.
    def MakeNode(self, tree):
        return self.GetBranchedNode(tree).add_variable(self.ServerNamespace, self.GetEndNode(tree), 1)

    # Return last Node name
    def GetEndNode(self, tree):
        return tree.split(".")[-1]

    # Create new branches to the end node
    # JG.WHG.OG.LR.SOCKET01.OM.B_VALUE
    def GetBranchedNode(self, tree):
        branches = tree.split(".")
        branchAddress = ""
        branchIndex = 1
        parentNode = self.root
        delim = ""
        del branches[-1]
        for branch in branches:
            branchAddress = branchAddress + delim + branch
            if not branchAddress in self.tree:
                parentNode = parentNode.add_object(self.ServerNamespace, branch)
                self.tree[branchAddress] = parentNode
            else:
                parentNode = self.tree[branchAddress]
            delim = "."
            branchIndex = branchIndex + 1
        return parentNode
