# RelayItem fields.
class BaseItem:
    opcitem_id = ""
    opcitem_created = ""
    opcitem_modified = ""
    opcitem_flag = ""
    opcitem_address = ""
    server_id = ""
    opcitem_datatype = ""
    opcitem_lastvalue = ""
    LocalNode = ""
    RemoteNode = ""

    def __init__(self, row):
        self.opcitem_id = row[0]
        self.opcitem_created = row[1]
        self.opcitem_modified = row[2]
        self.opcitem_flag = row[3]
        self.opcitem_address = row[4]
        self.server_id = row[5]
        self.opcitem_datatype = row[6]
        self.opcitem_lastvalue = row[7]
