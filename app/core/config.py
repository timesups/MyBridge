import os
from tinydb import TinyDB, Query
import shutil
import hashlib
import json
import win32file

def is_used(file_name):
    try:
        vHandle = win32file.CreateFile(file_name,win32file.GENERIC_READ,0,None,win32file.OPEN_EXISTING,win32file.FILE_ATTRIBUTE_NORMAL,None)
        return int(vHandle) == win32file.INVALID_HANDLE_VALUE
    except:
        return True
    finally:
        try:
            win32file.CloseHandle(vHandle)
        except:
            pass
def calculate_md5(file_path, block_size=65536):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            md5.update(block)
    return md5.hexdigest()


class Config():
    instance = None
    def __init__(self) -> None:
        self.localAssetLibraryFolder = os.path.join(os.environ['USERPROFILE'], 'Documents',"MyBridge")
        self.localDataBsePath = os.path.join(self.localAssetLibraryFolder,"AssetDataCache.json")
        self.localTempFolder = os.path.join(self.localAssetLibraryFolder,"Temp")
        self.localConfigSavePath = os.path.join(self.localAssetLibraryFolder,"config.json")

        # can saved value
        self.remoteAssetLibraryFolder = "E:\AssetLibrary"
        self.sockeAddress = "127.0.0.1"
        self.socketSendPort = 54321
        self.exportTextureSizeIndex = 0
        self.exportLodIndex = 0


        self.loadConfig()

        self.remoteDataBasepath = os.path.join(self.remoteAssetLibraryFolder,"AssetDataCache.json")
        self.remoteAssetLibrary = os.path.join(self.remoteAssetLibraryFolder,"Assets")
        self.__createFolders()

    def loadConfig(self):
        if not os.path.exists(self.localConfigSavePath):
            return
        with open(self.localConfigSavePath,'r',encoding="utf-8") as f:
            data = json.loads(f.read())
        try:
            self.remoteAssetLibraryFolder = data["remoteAssetLibraryFolder"]
            self.sockeAddress = data["sockeAddress"]
            self.socketSendPort = data["socketSendPort"]
            self.exportTextureSizeIndex = data["exportTextureSizeIndex"]
            self.exportLodIndex = data["exportLodIndex"]
        except KeyError:
            pass
    def saveConfig(self):
        data = dict(
            remoteAssetLibraryFolder = self.remoteAssetLibraryFolder,
            sockeAddress = self.sockeAddress,
            socketSendPort = self.socketSendPort,
            exportTextureSizeIndex = self.exportTextureSizeIndex,
            exportLodIndex = self.exportLodIndex
        )
        with open(self.localConfigSavePath,'w+',encoding="utf-8") as f:
            f.write(json.dumps(data))

    def __createFolders(self):
        folders = [
            self.remoteAssetLibraryFolder,
            self.remoteAssetLibrary,
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