import requests
from .config import Config
import app.core.utility as ut
import json
from app.core.Log import Log

class Backend():
    instance = None
    def __init__(self):
        pass
    def isBackendAvailable(self) -> bool:
        try:
            response = requests.get(Config.Get().backendAddress,timeout=3)
            return True
        except:
            return False
    def getCategories(self):
        response = requests.get(Config.Get().backendAddress+"/config/category")
        return response.json()
    def getAssetRootPath(self):
        response = requests.get(Config.Get().backendAddress+"/config/assetsLibraryPath")
        return response.json()["uri"]
    def getAssetsList(self)->list:
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
    def check_update(self):
        if not Backend.Get().isBackendAvailable():
            Log(f"服务器连接失败,停止获取更新","backend")
            return 
        #检查更新
        Log("开始检查更新","backend")
        exePath = ut.GetExePath()
        if not exePath:
            Log("当前尚未打包,跳过更新")
            return False
        version = ut.getExeVersion(exePath)
        Log(f"当前程序的版本为{version}","backend")
        response = requests.get(Config.Get().backendAddress+f"/update/check/{version}")
        result = json.loads(response.text)['result']
        if not result:
            Log(f"当前版本不需要更新","backend")
            return False
        Log(f"当前版本需要更新,开始获取最新版本","backend")
        response = requests.get(Config.Get().backendAddress+f"/update/new")
        newest_version = json.loads(response.text)['version']
        Log(f"最新版本获取成功,版本号为{newest_version}","backend")
        return newest_version
    def download_version(self,version):
        import os
        save_path = os.path.join(Config.Get().localTempFolder,"installer.exe")
        #删除老版本,如果存在
        if os.path.exists(save_path):
            os.remove(save_path)
        Log(f"准备开始版本{version}","backend")
        response = requests.get(Config.Get().backendAddress+f"/update/download/{version}")
        response.raise_for_status()
        with open(save_path,'wb') as f:
            f.write(response.content)
        return save_path

    def changeAsset(self,assetID,attrname:str,value):
        response = requests.post(Config.Get().backendAddress+f"/assets/change",json=dict(attrname=attrname,value=value,assetID=assetID))
    @classmethod
    def Get(cls):
        if cls.instance is None:
            cls.instance = Backend()
        return cls.instance

