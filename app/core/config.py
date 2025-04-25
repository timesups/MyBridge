import os
import json

class Config():
    instance = None
    def __init__(self) -> None:
        self.localAssetLibraryFolder = os.path.join(os.environ['USERPROFILE'], 'Documents',"MyBridge")
        self.localTempFolder = os.path.join(self.localAssetLibraryFolder,"Temp")
        self.localConfigSavePath = os.path.join(self.localAssetLibraryFolder,"config.json")

        # can saved value
        self.sockeAddress = "127.0.0.1"
        self.socketSendPort = 54321
        self.exportTextureSizeIndex = 0
        self.exportLodIndex = 0
        self.backendAddress = "http://192.168.3.133:5050"

        self.loadConfig()
        self.__createFolders()

    def loadConfig(self):
        if not os.path.exists(self.localConfigSavePath):
            return
        with open(self.localConfigSavePath,'r',encoding="utf-8") as f:
            data = json.loads(f.read())
        try:
            self.sockeAddress = data["sockeAddress"]
            self.socketSendPort = data["socketSendPort"]
            self.exportTextureSizeIndex = data["exportTextureSizeIndex"]
            self.exportLodIndex = data["exportLodIndex"]
            self.backendAddress = data["backendAddress"]
        except KeyError:
            pass
    def saveConfig(self):
        data = dict(
            sockeAddress = self.sockeAddress,
            socketSendPort = self.socketSendPort,
            exportTextureSizeIndex = self.exportTextureSizeIndex,
            exportLodIndex = self.exportLodIndex,
            backendAddress = self.backendAddress
        )
        with open(self.localConfigSavePath,'w+',encoding="utf-8") as f:
            f.write(json.dumps(data))

    def __createFolders(self):
        folders = [
            self.localAssetLibraryFolder,
            self.localTempFolder
        ]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
    def getSendSocketAddress(self)->tuple[str,int]:
        return (self.sockeAddress,self.socketSendPort)
    @classmethod
    def Get(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance