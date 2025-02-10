from tinydb import TinyDB,Query
import win32file
import os
import shutil
import hashlib
import time

from app.core.config import Config

def calculate_md5(file_path, block_size=65536):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            md5.update(block)
    return md5.hexdigest()


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


class DataBase():
    def __init__(self,path:str) -> None:
        self.dataBasePath = path
        self.dataBase = None
        self.isUsed = False
    def UseDataBase(self):
        self.dataBase = TinyDB(self.dataBasePath)
        self.isUsed = True
    def releaseDataBase(self):
        self.dataBase.close()
        self.isUsed = False
    def addAssetToDB(self,assetData:dict):
        self.dataBase.insert(assetData)
    def deleteAssetFromDB(self,assetID):
        user = Query()
        self.dataBase.remove(user.AssetID==assetID)
    def DataBaseAssetCount(self) ->int:
        return(len(self.dataBase.all()))
    def isAssetInDB(self,id:str):
        user = Query()
        result = self.dataBase.search(user.AssetID == id)
        if result == []:
            return False
        return result
    def getAllAssets(self):
        return self.dataBase.all()
    def Update(self,assetID:str,data:dict):
        user = Query()

        self.dataBase.update(dict,user.AssetID==assetID)
    
class DataBaseLocal(DataBase):
    instance = None
    def __init__(self) -> None:
        super().__init__(Config.Get().localDataBsePath)
    def syncDataBaseFromRemote(self):
        if os.path.exists(Config.Get().remoteDataBasepath):
            if os.path.exists(self.dataBasePath) and (calculate_md5(self.dataBasePath) != calculate_md5(Config.Get().remoteDataBasepath)):
                if self.isUsed:
                    self.releaseDataBase()
                os.remove(self.dataBasePath)
            else:
                return
            #当远程库不被占用的时候再同步数据
            while 1:
                if not DataBaseRemote.Get().isRemoteDataBaseInUsed():
                    shutil.copyfile(Config.Get().remoteDataBasepath,self.dataBasePath)
                    break
                else:
                    time.sleep(1)
        elif os.path.exists(self.dataBasePath):
            if not self.isUsed:
                os.remove(self.dataBasePath)
            DataBaseRemote().Get().UseDataBase()
            DataBaseRemote().Get().releaseDataBase()
        else:
            pass

    @classmethod
    def Get(cls):
        if not cls.instance:
            cls.instance = cls()
        cls.instance.syncDataBaseFromRemote()
        if not cls.instance.isUsed:
            cls.instance.UseDataBase()
        return cls.instance
    

class DataBaseRemote(DataBase):
    instance = None
    def __init__(self) -> None:
        super().__init__(Config.Get().remoteDataBasepath)
    def isRemoteDataBaseInUsed(self):
        return is_used(self.dataBasePath)
    @classmethod
    def Get(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance
