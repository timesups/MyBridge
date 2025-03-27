import app.core.ImportBridgeAsset as ib
import app.core.utility as ut
from app.core.datebase import DataBaseRemote
from app.core.config import Config
import os
import json

def ImportBridgeAssets():
    rootPath = r"\\192.168.3.126\uecache\项目素材\Quixel_Textures\Megascans Library\Downloaded"
    ib.ImportBridgeAssetFromDir(rootPath)

def UpdateAssetLibrary():
    DataBaseRemote.Get().UseDataBase()
    assets = DataBaseRemote.Get().getAllAssets()
    DataBaseRemote.Get().releaseDataBase()
    for assetData in assets:
        jsPath = os.path.join(Config.Get().remoteAssetLibrary,assetData["rootFolder"],assetData['jsonUri'])
        with open(jsPath,'r',encoding='utf-8') as f:
            asset = ut.Asset.from_dict(json.loads(f.read()))
        for tag in asset.tags:
            if tag in ut.GetCategorys(1):
                asset.subcategory = tag
                for p in ut.GetCategorys(0):
                    if tag in ut.category[p]:
                        asset.category = p
                break
            else:
                categorys = ut.GetParentsCategory(tag)
                if categorys: 
                    asset.category = categorys[0]
                    asset.subcategory = categorys[1]
                    break
        with open(jsPath,'w+',encoding='utf-8') as f:
            f.write(json.dumps(asset.to_dict()))
        DataBaseRemote.Get().UseDataBase()
        DataBaseRemote.Get().deleteAssetFromDB(asset.AssetID)
        DataBaseRemote.Get().releaseDataBase()
        ut.AddAssetDataToDataBase(asset)



if __name__ == "__main__":
    ImportBridgeAssets()
    