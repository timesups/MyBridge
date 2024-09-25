import os
from tinydb import TinyDB, Query
import shutil
import hashlib


def calculate_md5(file_path, block_size=65536):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            md5.update(block)
    return md5.hexdigest()


class Config:
    instance = None
    def __init__(self) -> None:
        self.remoteAssetLibraryFolder = "E:\AssetLibrary"
        self.remoteDataBasepath = os.path.join(self.remoteAssetLibraryFolder,"AssetDataCache.json")
        self.remoteAssetLibrary = os.path.join(self.remoteAssetLibraryFolder,"Assets")

        self.localAssetLibraryFolder = os.path.join(os.environ['USERPROFILE'], 'Documents',"MyBridge")
        self.localDataBsePath = os.path.join(self.remoteAssetLibraryFolder,"AssetDataCache.json")
        self.localAssetLibrary = os.path.join(self.remoteAssetLibraryFolder,"Assets")

        self.localTempFolder = os.path.join(self.localAssetLibraryFolder,"Temp")



        # 向UE发送消息所需的参数
        self.sockeAddress = "127.0.0.1"
        self.socketSendPort = 54321

        # 创建所需要的目录
        self.__createFolders()
        # 从服务器同步数据库
        self.syncDataCache()
        # 初始化数据库
        self.__initDataBse()
    def __initDataBse(self):
        self.remoteDataBase = TinyDB(self.remoteDataBasepath)
        if os.path.exists(self.localDataBsePath):
            self.localDataBase = TinyDB(self.localDataBsePath)
        else:
            self.localDataBase = None
    def getSendSocketAddress(self)->tuple[str,int]:
        return (self.sockeAddress,self.socketSendPort)
    def syncDataCache(self):
        if os.path.exists(self.remoteDataBasepath):
            if not os.path.exists(self.localDataBsePath):
                shutil.copyfile(self.remoteDataBasepath,self.localDataBsePath)
                return
            if calculate_md5(self.localDataBsePath) != calculate_md5(self.remoteDataBasepath):
                os.remove(self.localDataBsePath)
                shutil.copyfile(self.remoteDataBasepath,self.localDataBsePath)
                return
    def isIDinDB(self,id:str):
        user = Query()
        result = self.remoteDataBase.search(user.AssetID == id)
        if result == []:
            return False
        return result
    def addAssetToDB(self,assetData:dict):
        self.remoteDataBase.insert(assetData)
    def getAllAssets(self):
        if self.localDataBase:
            return self.localDataBase.all()
        else:
            return []
    def getCurrentAssetCount(self)->int:
        return len(self.remoteDataBase.all())
    def __createFolders(self):
        folders = [
            self.remoteAssetLibraryFolder,
            self.remoteAssetLibrary,
            self.localAssetLibraryFolder,
            self.localAssetLibrary,
            self.localTempFolder
        ]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
    @classmethod
    def Get(cls):
        if cls.instance == None:
            cls.instance = Config()
        return cls.instance