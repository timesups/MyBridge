import os
from tinydb import TinyDB, Query
import shutil
import hashlib
import json


def calculate_md5(file_path, block_size=65536):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            md5.update(block)
    return md5.hexdigest()


class Config:
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

        
        # 所有可以保存的数据需要在导入配置之前设置
        self.loadConfig()
        self.remoteDataBasepath = os.path.join(self.remoteAssetLibraryFolder,"AssetDataCache.json")
        self.remoteAssetLibrary = os.path.join(self.remoteAssetLibraryFolder,"Assets")

        # 创建所需要的目录
        self.__createFolders()

    def saveConfig(self):
        data = dict(
            remoteAssetLibraryFolder = self.remoteAssetLibraryFolder,
            sockeAddress = self.sockeAddress,
            socketSendPort = self.socketSendPort,
            exportTextureSizeIndex = self.exportTextureSizeIndex
        )
        with open(self.localConfigSavePath,'w+',encoding="utf-8") as f:
            f.write(json.dumps(data))
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
        except KeyError:
            pass
    def __initDataBase(self):
        self.remoteDataBase = TinyDB(self.remoteDataBasepath)
        if os.path.exists(self.localDataBsePath):
            self.localDataBase = TinyDB(self.localDataBsePath)
        else:
            self.localDataBase = None
    def getSendSocketAddress(self)->tuple[str,int]:
        return (self.sockeAddress,self.socketSendPort)
    def __syncDataCache(self):
        if os.path.exists(self.remoteDataBasepath):
            if not os.path.exists(self.localDataBsePath):
                shutil.copyfile(self.remoteDataBasepath,self.localDataBsePath)
                return
            if calculate_md5(self.localDataBsePath) != calculate_md5(self.remoteDataBasepath):
                try:
                    # 当前的本地资产库已经存在时需要解除占用才能从服务器正确同步数据库文件
                    self.localDataBase.close()
                    self.localDataBase = None
                except:
                    pass
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
        # 从服务器同步数据库
        self.__syncDataCache()
        # 初始化数据库
        self.__initDataBase()
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