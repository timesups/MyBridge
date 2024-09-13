from enum import Enum
import os
from dataclasses import dataclass,field



class MyBridgetGlobalEnum(Enum):
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
        return data
    def __repr__(self) -> str:
        return(str(self.to_dict()))
    @classmethod
    def from_dict(cls,data):
        asset = cls()
        for key in data.keys():
            obj = asset.__getattribute__(key)
            if isinstance(obj,MyBridgetGlobalEnum):
                asset.__setattr__(key,obj.__class__._value2member_map_[data[key]])
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
class LOD(SerializeBase):
    uri         : str          = field(default_factory=str)
    normalMap   : AssetMap     = field(default_factory=AssetMap)
@dataclass(repr=False)
class Asset(SerializeBase):
    name         :str               = field(default_factory=str)
    ZbrushFile   :str               = field(default_factory=str)
    AssetID      :str               = field(default_factory=str)

    tags         :list[str]         = field(default_factory=list[str])
    previewFilee :list[str]         = field(default_factory=list[str])
    Lods         :list[LOD]         = field(default_factory=list[LOD])
    maps         :list[AssetMap]    = field(default_factory=list[AssetMap])

    type         :AssetType         = field(default=AssetType.Assets3D)
    category     :AssetCategory     = field(default=AssetCategory.Building)
    subcategory  :AssetSubccategory = field(default=AssetSubccategory.Floating)
    urfaceSize   :AssetSize         = field(default=AssetSize.Meter1)

    TilesV       :bool              = field(default_factory=bool)
    TilesH       :bool              = field(default_factory=bool)

    AssetIndex   :int               = field(default_factory=int)


TextureExtensions = [".png",'.exr','.jpg']
def ClassifyFilesFormFolder(folder:str):
    models = []
    images = []
    zbrushs = []
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
        elif ext == ".ztl":
            zbrushs.append(zbrushs)
            pass
        if ext == ".jpg":
            assetName = basename
    return dict(assetName = assetName,images = images,models=models,zbrushs=zbrushs)

def MakeAssetByData(datas:dict)->Asset:
    asset = Asset()


    return asset

if __name__ == "__main__":
    print(ClassifyFilesFormFolder("d:\Desktop\Temp\Bmwl_1"))

    





    
