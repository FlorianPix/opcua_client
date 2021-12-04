class SubHandler(object):
    def __init__(self):
        self.var = None
        self.change = False

    def hasChanged(self):
        if self.change:
            change = True
        else:
            change = False
        self.change = False
        return change

    def getVar(self):
        return self.var

    def datachange_notification(self, node, val, data):
        # callback on a data change
        self.var = val
        if val is not None:
            self.change = True
