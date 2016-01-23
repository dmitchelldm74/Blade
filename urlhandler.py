import urllib
class urlhandler:
    address = ''
    data = ''
    def __init__(self, url):
        self.address = url
    def openURL(self):
        self.data =  urllib.urlopen(self.address)
    def getURLdata(self):
        return self.data.read()
    def closeURL(self):
        self.data.close()
