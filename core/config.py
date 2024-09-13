import os

class Config:
    instance = None
    def __init__(self) -> None:
        self.AssetLibraryRoot = "E:\AssetLibrary"
        self.AssetDatasCache = os.path.join(self.AssetLibraryRoot,"AssetDataCache.json")
        self.AssetLibrary = os.path.join(self.AssetLibraryRoot,"Assets")
        self.CurrentAssetIndex = 0
        self.__createFolders()
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