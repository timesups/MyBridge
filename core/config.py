import os
from tinydb import TinyDB, Query

class Config:
    instance = None
    def __init__(self) -> None:
        self.AssetLibraryRoot = "E:\AssetLibrary"
        self.AssetDatasCache = os.path.join(self.AssetLibraryRoot,"AssetDataCache.json")
        self.AssetLibrary = os.path.join(self.AssetLibraryRoot,"Assets")
        self.__createFolders()
        self.__initDB()
    def __initDB(self):
        self.dataBase = TinyDB(self.AssetDatasCache)
    def isIDinDB(self,id:str):
        user = Query()
        result = self.dataBase.search(user.AssetID == id)
        if result == []:
            return False
        return result
    def addAssetToDB(self,assetData:dict):
        self.dataBase.insert(assetData)
    def getCurrentAssetCount(self)->int:
        return len(self.dataBase.all())
    def __createFolders(self):
        if not os.path.exists(self.AssetLibraryRoot):
            os.makedirs(self.AssetLibraryRoot)
        if not os.path.exists(self.AssetLibrary):
            os.makedirs(self.AssetLibrary)
    @classmethod
    def Get(cls):
        if cls.instance == None:
            cls.instance = Config()
        return cls.instance