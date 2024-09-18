from enum import Enum
import os
from dataclasses import dataclass,field
from collections import OrderedDict
import random
import string
import shutil
import copy
import json
from core.config import Config

class MyBridgetGlobalEnum(Enum):
    def __format__(self, format_spec: str) -> str:
        return super().__format__(format_spec)
    pass
class AssetType(MyBridgetGlobalEnum):
    Assets3D = "3D Assets"
    Surface = "Surface"

class AssetCategory(MyBridgetGlobalEnum):
    Building   = "Building"
    Food       = "Food"
    Historical = "Historical"
    Industrial = "Industrial"

class AssetSubccategory(MyBridgetGlobalEnum):
    Floating = "Floating"
    Shore    = "Shore"
    Submerged = "Submerged"

class AssetSize(MyBridgetGlobalEnum):
    Meter1 = "1 Meter"
    Meters2 = "2 Meters"
    Meters3 = "3 Meters"
    Meters4 = "4 Meters"

class AssetFormat(MyBridgetGlobalEnum):
    UnrealEngine = "Unreal Engine"
    FBX          = "FBX"

class AssetMapType(MyBridgetGlobalEnum):
    Albedo = "Albedo"
    AO = "AO"
    Brush = "Brush"
    Bump = "Bump"
    Cavity = "Cavity"
    Diffuse = "Diffuse"
    Displacement = "Displacement"
    Fuzz = "Fuzz"
    Gloss = "Gloss"
    Mask = "Mask"
    Metalness = "Metalness"
    Normal = "Normal"
    Opacity = "Opacity"
    Roughness = "Roughness"
    Specular = "Specular"
    Translucency = "Translucency"



@dataclass(repr=False)
class SerializeBase:
    def to_dict(self):
        data = self.__dict__
        for key in data.keys():
            if isinstance(data[key],MyBridgetGlobalEnum):
                data[key] = data[key].value
            elif isinstance(data[key],SerializeBase):
                data[key] = data[key].to_dict()
            elif isinstance(data[key],list):
                for i in range(len(data[key])):
                    try:
                        data[key][i] = data[key][i].to_dict()
                    except:
                        pass
        return data
    def __repr__(self) -> str:
        return(str(self.to_dict()))
    @classmethod
    def from_dict(cls,data):
        asset = cls()
        for key in data.keys():
            obj = asset.__getattribute__(key)
            if isinstance(obj,MyBridgetGlobalEnum):
                asset.__setattr__(key,copy.deepcopy(obj.__class__._value2member_map_[data[key]]))
            elif isinstance(obj,SerializeBase):
                asset.__setattr__(key,obj.__class__.from_dict(data[key]))
            elif isinstance(obj,list):
                itemClass = cls.__annotations__[key].__args__[0]
                if isinstance(itemClass(),SerializeBase):
                    for item in data[key]:
                        asset.__getattribute__(key).append(itemClass.from_dict(item))
                else:
                    asset.__setattr__(key,data[key])
            else:
                asset.__setattr__(key,data[key])
        return asset

@dataclass(repr=False)
class AssetMap(SerializeBase):
    uri         : str          = field(default_factory=str)
    extension   : str          = field(default_factory=str)
    name        : str          = field(default_factory=str)
    type        : AssetMapType = field(default=AssetMapType.Albedo)
    subMapCount : int          = field(default_factory=int) 
    UDIM        : bool         = field(default_factory=bool)
@dataclass(repr=False)
class AssetMesh(SerializeBase):
    uri         : str          = field(default_factory=str)
    name         : str          = field(default_factory=str)
    extension   : str          = field(default_factory=str)
@dataclass(repr=False)
class LOD(SerializeBase):
    mesh         : AssetMesh          = field(default_factory=AssetMesh)
    normalMap    : AssetMap           = field(default_factory=AssetMap)
    level        : int                = field(default_factory=int)
    def findLodNormal(self):
        lodMeshUri = self.mesh.uri
        lodMeshFolder = os.path.dirname(lodMeshUri)
        normalFileName = ""
        for file in os.listdir(lodMeshFolder):
            if "normal" in file.lower() and "lod" in file.lower():
                if str(self.level) in file:
                    normalFileName = file
                    break
        if normalFileName != "":
            self.normalMap.uri = os.path.join(lodMeshFolder,normalFileName)
            self.normalMap.name,self.normalMap.extension = os.path.splitext(normalFileName)
            self.normalMap.type = AssetMapType.Normal
            self.normalMap.subMapCount = 1
            self.normalMap.UDIM = False

@dataclass(repr=False)
class Asset(SerializeBase):
    name         : str               = field(default_factory=str)
    ZbrushFile   : str               = field(default_factory=str)
    AssetID      : str               = field(default_factory=str)
    rootFolder   : str               = field(default_factory=str)
    JsonUri      : str               = field(default_factory=str)

    tags         : list[str]         = field(default_factory=list[str])
    previewFile  : list[str]         = field(default_factory=list[str])
    Lods         : list[LOD]         = field(default_factory=list[LOD])
    maps         : list[AssetMap]    = field(default_factory=list[AssetMap])

    type         : AssetType         = field(default=AssetType.Assets3D)
    category     : AssetCategory     = field(default=AssetCategory.Building)
    subcategory  : AssetSubccategory = field(default=AssetSubccategory.Floating)
    surfaceSize  : AssetSize        = field(default=AssetSize.Meter1)
    OriginMesh   : AssetMesh         = field(default_factory=AssetMesh)

    TilesV       : bool              = field(default_factory=bool)
    TilesH       : bool              = field(default_factory=bool)

    AssetIndex   : int               = field(default_factory=int)


TextureExtensions = [".png",'.exr','.jpg']
def ClassifyFilesFormFolder(folder:str):
    models = []
    images = []
    assetName = ''

    files = os.listdir(folder)
    for file in files:
        basename,ext = os.path.splitext(file)
        ext = ext.lower()
        filePath = os.path.join(folder,file)
        if not os.path.isfile(filePath):
            continue #跳过目录
        # 根据拓展名分类文件类型
        if ext in TextureExtensions:
            images.append(filePath)
            pass
        elif ext == ".fbx":
            models.append(filePath)
            pass
        if ext == ".jpg":
            assetName = basename
    return dict(assetName = assetName,images = images,models=models)

def MakeAssetByData(datas:dict)->Asset:
    asset = Asset()
    asset.name = datas["name"]
    asset.tags = [tag for tag in datas["tags"].split(",")]
    asset.type = copy.deepcopy(AssetType._value2member_map_[datas["type"]])
    for mapType in datas["mapData"].keys():
        mapPath = datas["mapData"][mapType]
        # 跳过不存在的贴图
        if mapPath == "":
            continue
        assetMap = AssetMap()
        assetMap.type = copy.deepcopy(AssetMapType._value2member_map_[mapType])
        assetMap.name,assetMap.extension = os.path.splitext(os.path.basename(mapPath))
        assetMap.uri = mapPath
        assetMap.subMapCount = 1
        assetMap.UDIM = False
        asset.maps.append(assetMap)
    if asset.type == AssetType.Assets3D:
        asset.OriginMesh = AssetMesh()
        asset.OriginMesh.uri = datas["orginMesh"]
        asset.OriginMesh.name,asset.OriginMesh.extension = os.path.splitext(os.path.basename(datas["orginMesh"]))
        for i in range(len(datas["lods"])):
            lod = LOD()
            lod.mesh = AssetMesh()
            lod.mesh.uri = datas["lods"][i]
            lod.mesh.name,lod.mesh.extension = os.path.splitext(os.path.basename(lod.mesh.uri))
            lod.level = i
            lod.findLodNormal()
            asset.Lods.append(lod)
        zbrushFileUri = asset.OriginMesh.uri.replace("fbx","ZTL")
        if os.path.exists(zbrushFileUri):
            asset.ZbrushFile = zbrushFileUri
    elif asset.type == AssetType.Surface:
        pass
    else:
        pass
    asset.previewFile.append(datas["previewImage"])
    return asset

def generate_random_string(length=10):
    # 定义生成随机字符串的字符集
    characters = string.ascii_letters + string.digits
    # 使用 random.choices 从字符集中随机选择字符，形成指定长度的字符串
    random_string = ''.join(random.choices(characters, k=length))
    return random_string
def generate_unique_string(length=10):
    while(1):
        random_string = generate_random_string(length)
        if not Config.Get().isIDinDB(random_string):
            return random_string
def CopyFileToFolder(filePath:str,folder:str,newName:str = None):
    newFileName = os.path.basename(filePath)
    if newName:
        newFileName = newName
    newFilePath = os.path.join(folder,newFileName)
    shutil.copyfile(filePath,newFilePath)
    return newFilePath
def CopyAndRenameAsset(asset:Asset):
    asset.AssetID = generate_unique_string(7)
    asset.rootFolder = os.path.join(Config.Get().AssetLibrary,f"{asset.name}_{asset.AssetID}")
    if not os.path.exists(asset.rootFolder):
        os.makedirs(asset.rootFolder)
    asset.AssetIndex = Config.Get().getCurrentAssetCount()
    asset.JsonUri = os.path.join(asset.rootFolder,f"{asset.AssetID}.json")
    for i in range(len(asset.Lods)):
        asset.Lods[i].mesh.name = f"{asset.AssetID}_LOD{asset.Lods[i].level}{asset.Lods[i].mesh.extension}"
        asset.Lods[i].mesh.uri = CopyFileToFolder(asset.Lods[i].mesh.uri,asset.rootFolder,asset.Lods[i].mesh.name)
        asset.Lods[i].normalMap.name = f"{asset.AssetID}_Normal_LOD{asset.Lods[i].level}{asset.Lods[i].normalMap.extension}"
        asset.Lods[i].normalMap.uri = CopyFileToFolder(asset.Lods[i].normalMap.uri,asset.rootFolder,asset.Lods[i].normalMap.name)
    asset.OriginMesh.name = asset.AssetID + asset.OriginMesh.extension
    asset.OriginMesh.uri = CopyFileToFolder(asset.OriginMesh.uri,asset.rootFolder,asset.OriginMesh.name)
    asset.ZbrushFile = CopyFileToFolder(asset.ZbrushFile,asset.rootFolder,f"{asset.AssetID}.ZTL")
    for i in range(len(asset.maps)):
        asset.maps[i].name = f"{asset.AssetID}_{asset.maps[i].type.value}{asset.maps[i].extension}"
        asset.maps[i].uri = CopyFileToFolder(asset.maps[i].uri,asset.rootFolder,asset.maps[i].name)
    asset.JsonUri = os.path.join(asset.rootFolder,asset.OriginMesh.name.replace(".fbx",'.json'))
    with open(asset.JsonUri,'w+',encoding='utf-8') as f:
        f.write(json.dumps(asset.to_dict()))
    Config.Get().addAssetToDB(asset.to_dict())
    pass
if __name__ == "__main__":
    print(ClassifyFilesFormFolder("d:\Desktop\Temp\Bmwl_1"))

    





    
