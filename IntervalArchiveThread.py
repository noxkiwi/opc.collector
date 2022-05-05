import sqlite3
import threading
import time
import sys
from datetime import datetime

from ArchiveThread import ArchiveThread
from DatabaseManager import DatabaseManager
from GroupItem import GroupItem
from noxLogger import noxLogger


# I am an interval based ArchiveThread
class IntervalArchiveThread(ArchiveThread):
    def __init__(self, group_row, base_client):
        super().__init__(group_row, base_client)
        self.DatabaseManager = DatabaseManager()
        self.GroupItem = GroupItem(group_row, self)
        noxLogger.debug("0x00030111 Create ArchiveThread for group " + self.GroupItem.GroupName)
        self.BaseClient = base_client
        self.Subscription = self.BaseClient.create_subscription(500, self.SubscriptionHandler)
        noxLogger.debug("0x00030012 Created ArchiveThread for group " + self.GroupItem.GroupName)
        self.scanEnable = False
        self.saveThread = threading.Thread(target=self.runThread)
        self.saveThread.start()

    # I am the list of fieldNames and fieldValues for the next entry in the archive db.
    fields = {}
    # I am the save thread.
    saveThread = None

    # I am the main thread method.
    # I will save the current data and will then wait for the GroupItem's interval to pass.
    # After that, I will run again.
    def runThread(self):
        # Take note when the process started
        self.started = time.process_time()
        # INITIALLY wait the ONE interval to fetch initial process-values first.
        time.sleep(self.GroupItem.GroupInterval / 1000)
        # THEN start the scanner.
        while self.ScanEnable:
            # Take note of the start time to save the entry.
            start = time.process_time()
            # Save the entry to DB.
            self.saveEntry()
            # Now we know how much time passed.
            elapsed = time.process_time() - start
            # Subtract the elapsed time from the interval to keep the interval straight.
            remaining = self.GroupItem.GroupInterval - elapsed
            # TODO Fix the origin of the connection timeout for subscriptions.
            # TODO Otherwise fix the issue by catching the error accordingly.
            # Now wait for the remaining time of the interval.
            time.sleep(remaining / 1000)

    # I am triggered from the subscription to update the given fields value for the next interval to be stored.<
    def subscriptionTriggered(self, field, value):
        self.fields[field] = value

    # I will save the current entry.
    def saveEntry(self):
        sql_fields = ""
        sql_values = ""
        sql_comma = ""

        # Add every single Item's field and value to the query strings.
        for fieldName in self.fields.keys():
            sql_fields = sql_fields + sql_comma + "`" + fieldName + "`"
            sql_values = sql_values + sql_comma + str(self.fields[fieldName])
            sql_comma = ", "

        # Use the previously filled vars to formulate MySQL.
        queryString = "INSERT INTO `" + self.GroupItem.GroupTable + "` (" + sql_fields + ") VALUES (" + sql_values + ");"
        queryData = (1, 2, 3)

        # Put stuph into the database.
        try:
            self.DatabaseManager.query(queryString, queryData)
            noxLogger.debug("0x00031011 Database query " + queryString + " successful.")
        except Exception as ex:
            noxLogger.error("0x00031012 Database query " + queryString + " with error.")
            return False
        return True
