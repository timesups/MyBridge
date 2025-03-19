import requests
from .config import Config
import json


class Backend():
    instance = None
    def __init__(self):
        pass
    def isBackendAvailable(self) -> bool:
        try:
            response = requests.get(Config.Get().backendAddress)
            return True
        except:
            return False
    def getCategories(self):
        response = requests.get(Config.Get().backendAddress+"/config/category")
        return response.json()
    def getAssetRootPath(self):
        response = requests.get(Config.Get().backendAddress+"/config/assetsLibraryPath")
        return response.json()["uri"]
    def getAssetsList(self):
        response = requests.get(Config.Get().backendAddress+"/assets/all")
        return response.json()
    def getAssetsCount(self):
        response = requests.get(Config.Get().backendAddress+"/assets/count")
        return response.json()
    def addAssetToDB(self,asset:dict):
        response = requests.post(Config.Get().backendAddress+"/assets/add",json=asset)
        return response.text
    def deleteAssetFromDB(self,assetID:str):
        response = requests.delete(Config.Get().backendAddress+f"/assets/delete/{assetID}")
        return response.text
    def getAsset(self,assetID:str):
        response = requests.get(Config.Get().backendAddress+f"/assets/{assetID}")
        if response.text != "false":
            return response.json()
        else:
            return False
    def changeAsset(self,assetID,attrname:str,value):
        response = requests.post(Config.Get().backendAddress+f"/assets/change",json=dict(attrname=attrname,value=value,assetID=assetID))
    @classmethod
    def Get(cls):
        if cls.instance is None:
            cls.instance = Backend()
        return cls.instance
    