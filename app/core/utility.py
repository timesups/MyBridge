import os
import random
import string
import shutil
import copy
import json
from PIL import Image,ImageFile
import pyexr
import Imath
import numexpr as ne
import socket
from tinydb import TinyDB, Query
import sys
from qfluentwidgets import Dialog
from win32com.client import Dispatch
import zipfile
from app.core.config import Config
from app.core.datebase import DataBaseRemote,DataBaseLocal

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import time
from enum import Enum
from dataclasses import dataclass,field

from app.core.Log import Log


UPDATE_SERVE_PATH = r"\\192.168.3.252\中影年年文化传媒有限公司\6动画基地\制作中心\地编组\Z_赵存喜\MyBirdge\update"
TextureExtensions = [".png",'.exr','.jpg']
FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)

class MyBridgetGlobalEnum(Enum):
    def __format__(self, format_spec: str) -> str:
        return super().__format__(format_spec)
    
class ComparableEnum(MyBridgetGlobalEnum):
    def GetValue(self,var):
        #子类需要对这个函数进行实现
        raise
    def __lt__(self,other):
        return self.GetValue(self) < self.GetValue(other)
    def __gt__(self,other):
        return self.GetValue(self) > self.GetValue(other)
    def __eq__(self,other):
        return self.GetValue(self) == self.GetValue(other)
    def __ge__(self,other):
        return self.GetValue(self) >= self.GetValue(other)
    def __le__(self,other):
        return self.GetValue(self) <= self.GetValue(other)
    def __int__(self):
        return self.GetValue(self)

class TextureSize(ComparableEnum):
    _2k = "2K"
    _4k = "4K"
    _8K = "8K"
    def GetValue(self,var):
         return eval(var.value[0])
    
class AssetType(MyBridgetGlobalEnum):
    Assets3D = "3D Assets"
    Surface = "Surface"
    Decal   = "Decal"
    Plant   = "Plant"
    Brush   = "brush"

class Format(MyBridgetGlobalEnum):
    FBX = "Fbx"
    Unreal = "Unreal"
       
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
    Curvature = "curvature"
    Transmission = "transmission"
    Thickness    = "thickness"


category = {
    "自然生态":{
        "森林植被":[
            "植物",
            "树叶",
            "树干树桩",
            "树枝干",
            "树皮",
            "森林地面",
            "苔藓材质",
        ],
        "山地丘陵":[
            "岩石块",
            "山地岩石壁",
            "山土地皮",
            "山地地面",
        ],
        "沙漠戈壁":[
            "沙漠材质",
            "土堆地面",
            "岩石坡",
            "沙漠岩石",
            "岩壁"
        ],
        "高原":[
            "石坡",
            "高原地面",
            "高原岩石"
        ],
        "海岸":[
            "沙滩",
            "地表材质",
            "海岸岩石",
            "海岸岩石壁"
        ],
        "河谷":[
            "河谷岩石",
            "河谷地面"
        ],
        "土壤":[

        ],
        "碎石地":[

        ],
        "雪地":[

        ],
    },
    "设置构建":{
        "工厂厂房":[
            "工厂标牌",
            "管道",
            "门窗",
            "罐状物",
            "沙袋",
            "集装箱",
            "结构件",
            "工业漆墙",
            "工业金属",
            "设备用具"
        ],
        "交通设施":[
            "标识",
            "插线",
            "船只",
            "摩托车",
            "自行车",
            "轨道",
            "路障",
        ],
        "城市街区":[
            "街道路面",
            "台阶道路",
            "公共设置",
            "标牌",
            "城市门窗面板",
            "墙体",
            "样式材质",
            "地面",
            "垃圾"
        ],
        "山村城镇":[
            "城镇门窗面板",
            "屋顶",
            "线路管道",
            "行牌贴纸",
            "墩状物",
            "柱状物",
            "护栏",
            "路面",
            "墙体"  
            "道具",
            "台阶道路",
            "盒装设施",
            "农工农具",
            "木条木架",
            "建筑结构",
        ],
        "中式结构":[
            "屋檐屋顶",
            "雕像",
            "浮雕",
            "柱体",
            "地台",
            "横梁",
            "门窗",
            "梁托",
            "牌匾"
            "围边",
            "门楣",
            "塔鼎",
            "矮柱",
            "神龛",
            "阶梯",
            "护栏",
            "景观奇石",
            "石碑"
            "木质表面",
            "地砖材质",
            "砖墙材质",
            "其他结构",
        ],
        "废旧设施":[
            "破损地板",
            "设备",
            "道具",
            "地面材质",
            "墙体土块",
            "块状物",
            "腐蚀地面",
            "面板",
            "地摊"
        ],
        "欧式结构":[

        ],
    },
    "商品货物":{
        "家居用品":[
            "凳子",
            "缸类",
            "桶",
            "碗",
            "文具书籍",
            "杯子",
            "瓶罐",
            "钟表类"
            "欧式家具",
            "现代家具",
            "中式家具",
            "仓储柜",
            "灯具",
            "生活用品",
            ],
        "家具材质":[
            "木材类",
            "编织类",
            "地砖瓷砖",
		],
        "电子设备":[
		],
        "货物包装":[
            "包装纸盒",
            "铁皮盒",
            "快递包装",
		],
        "农产品":[
            "浆果类",
            "坚果类",
            "瓜果类",
            "蔬菜类",
            "仁核果类",
            "柑橘类",
            "根茎类",
            "菌类",
            "鲜豆类",
            "香料",
		],
        "餐饮美食":[
            "面包",
            "糕点",
            "肉类",
            "豆制品",
		],
        "服装穿搭":[
            "布料材质",
            "服装",
            "其他",
		],
    },
    "肌理特效":{
        "墙面破损":[
            "裂纹",
            "砖面",
            "墙皮",
            "裂痕",
		],
        "污渍":[
		],
        "喷涂":[
		],
        "涂画":[
            "数字字母",
            "涂鸦",
		],
        "贴纸":[
		],
        "地面破损":[
            "裂纹",
            "面片",
            "残渣",
		],
        "苔藓印记":[
		],
        "其他印记":[
		],
        "木制破损":[
		],
        "表面纹理":[
		],
        "腐蚀":[
		],
        "宣传口号":[
		],
    },
    "工艺制品":{
        "精致器皿":[
            "茶具类",
            "陶瓷盘类",
            "木器",
            "其他",
            "金属器",
            "陶瓷瓶罐",
		],
        "兵器与军工":[
		],
        "艺术创作":[
            "绘画",
            "壁画雕刻",
            "窗花",
		],
        "娱乐产品":[
            "乐器",
            "棋牌",
            "玩具",
		],
        "生物标本":[
		],
    },
}

def GetParentsCategory(name):
    for p in category.keys():
        for c in category[p].keys():
            for cc in category[p][c]:
                if name == cc:
                    return p,c,cc
    return False

def GetCategorys(level:int):
    if level == 0:
        return list(category.keys())
    elif level == 1:
        return [ele for value in category.values() for ele in value.keys() ]
    elif level == 2:
        return [c for value in category.values() for ele in value.keys() for c in value[ele]]
    else:
        raise


@dataclass(repr=False)
class SerializeBase:
    def to_dict(self):
        data = copy.deepcopy(self.__dict__)
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
    size        : TextureSize  = field(default=TextureSize._2k)
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
class Material(SerializeBase):
    name         : str               = field(default_factory=str)
    maps         : list[AssetMap]    = field(default_factory=list[AssetMap])
@dataclass(repr=False)
class MeshVar(SerializeBase):
    OriginMesh     : AssetMesh         = field(default_factory=AssetMesh)
    Lods           : list[LOD]         = field(default_factory=list[LOD])
    VarIndex       : int               = field(default_factory=int)
@dataclass(repr=False)
class Asset(SerializeBase):
    name           : str               = field(default_factory=str)
    ZbrushFile     : str               = field(default_factory=str)
    AssetID        : str               = field(default_factory=str)
    rootFolder     : str               = field(default_factory=str)
    JsonUri        : str               = field(default_factory=str)

    tags           : list[str]         = field(default_factory=list[str])
    previewFile    : list[str]         = field(default_factory=list[str])
    Lods           : list[LOD]         = field(default_factory=list[LOD])
    assetMaterials : list[Material]    = field(default_factory=list[Material])
    MeshVars : list[MeshVar]    = field(default_factory=list[MeshVar])

    type           : AssetType         = field(default=AssetType.Assets3D)
    category       : str               = field(default=GetCategorys(0)[0])
    subcategory    : str               = field(default=GetCategorys(1)[0])
    surfaceSize    : AssetSize         = field(default=AssetSize.Meter1)
    assetFormat    : AssetFormat       = field(default=AssetFormat.FBX)

    OriginMesh     : AssetMesh         = field(default_factory=AssetMesh)


    TilesV         : bool              = field(default_factory=bool)
    TilesH         : bool              = field(default_factory=bool)

    AssetIndex     : int               = field(default_factory=int)
    OldJson        : str               = field(default_factory=str)




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

def encode_to_srgb(x):
    a = 0.055
    return ne.evaluate("""where(
                            x <= 0.0031308,
                            x * 12.92,
                            (1 + a) * (x ** (1 / 2.4)) - a
                          )""")


def exr_to_srgb(exrfile):
    Log(f"将EXR转换为SRGB")
    try:
        array =  pyexr.read(exrfile)
    except:
        Log(f"EXR文件读取失败")
        return False
    Log(f"EXR文件读取成功")
    result = encode_to_srgb(array) * 255.
    present_channels = ["R", "G", "B", "A"][:result.shape[2]]
    channels = "".join(present_channels)
    if len(channels) == 1:
        channels = "L"
        result = result.mean(axis=2)
    try:
        Log(f"将EXR转换为SRGB完成")
        return Image.fromarray(result.astype('uint8'), channels)
    except:
        return False

def readImage(filePath)->ImageFile:
    Log(f"读取图片{filePath}")
    _,ext = os.path.splitext(filePath)
    if ext.lower() == '.exr':
        # image = exr_to_srgb(filePath)
        # if not image:
        #     return False
        return False
    else:
        try:
            image = Image.open(filePath)
        except:
            return False
    return image


def GetTextureSize(uri:str):
    image = readImage(uri)
    if not image:
        return False
    size = image.size
    maxSize = max(size[0],size[1])
    if maxSize >= 8192:
        return TextureSize._8K
    elif maxSize >= 4096:
        return TextureSize._4k
    else:
        return TextureSize._2k
def removeFolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

#进入此函数的所有路径需要保证完成规格化
def MakeAssetByData(datas:dict)->Asset:
    asset = Asset()
    asset.name = datas["name"]
    asset.tags = datas["tags"]

    asset.type = copy.deepcopy(AssetType._value2member_map_[datas["type"]])
    asset.category = datas["category"]
    asset.subcategory = datas["subCategory"]

    material = Material()
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
        assetMap.size = GetTextureSize(assetMap.uri)
        material.maps.append(assetMap)
        material.name = asset.name
    asset.assetMaterials.append(material)
    if asset.type == AssetType.Assets3D or asset.type == AssetType.Plant:
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
    elif asset.type == AssetType.Surface or asset.type == AssetType.Decal:
        asset.surfaceSize = copy.deepcopy(AssetSize._value2member_map_[datas["surfaceSize"]])
        asset.TilesV =  datas["TilesVertically"]
        asset.TilesH = datas["TillesHorizontically"]
    else:
        pass
    asset.previewFile.append(datas["previewImage"])
    asset.assetFormat = AssetFormat.FBX
    return asset

def CopyAndRenameAsset(asset:Asset):
    Log(f"Start to move asset {asset.name}","ImportAsset")
    DataBaseRemote.Get().UseDataBase()
    # 计算资产ID
    asset.AssetID = generate_unique_string(7)
    Log(f"Asset ID is :{asset.AssetID}","ImportAsset")
    # 创建资产根目录
    rootFolder = os.path.join(Config.Get().remoteAssetLibrary,f"{asset.AssetID}")
    Log(f"Asset root folder is :{rootFolder}","ImportAsset")
    asset.rootFolder = f"{asset.AssetID}"
    if not os.path.exists(rootFolder):
        os.makedirs(rootFolder)
    # 获取资产编号
    asset.AssetIndex = DataBaseRemote.Get().DataBaseAssetCount()

    #复制Bridge中原有的Json文件
    if asset.OldJson != "":
        asset.OldJson = CopyFileToFolder(asset.OldJson,rootFolder,f"{asset.AssetID}_old.json")

    if asset.type == AssetType.Assets3D or asset.type == AssetType.Plant:
        for i in range(len(asset.Lods)):
            asset.Lods[i].mesh.name = f"{asset.AssetID}_LOD{asset.Lods[i].level}{asset.Lods[i].mesh.extension}"
            asset.Lods[i].mesh.uri = CopyFileToFolder(asset.Lods[i].mesh.uri,rootFolder,asset.Lods[i].mesh.name)
            asset.Lods[i].normalMap.name = f"{asset.AssetID}_Normal_LOD{asset.Lods[i].level}{asset.Lods[i].normalMap.extension}"
            asset.Lods[i].normalMap.uri = CopyFileToFolder(asset.Lods[i].normalMap.uri,rootFolder,asset.Lods[i].normalMap.name)
        for i in range(len(asset.MeshVars)):
            var_sub_folder = os.path.join(rootFolder,f"Var{asset.MeshVars[i].VarIndex}")
            if not os.path.exists(var_sub_folder):
                os.makedirs(var_sub_folder)
            asset.MeshVars[i].OriginMesh.name = f"{asset.AssetID}_Var{asset.MeshVars[i].VarIndex}{asset.MeshVars[i].OriginMesh.extension}"
            asset.MeshVars[i].OriginMesh.uri = CopyFileToFolder(asset.MeshVars[i].OriginMesh.uri,var_sub_folder,asset.MeshVars[i].OriginMesh.name)
            for j in range(len(asset.MeshVars[i].Lods)):
                asset.MeshVars[i].Lods[j].mesh.name = f"{asset.AssetID}_Var{asset.MeshVars[i].VarIndex}_LOD{asset.MeshVars[i].Lods[j].level}{asset.MeshVars[i].OriginMesh.extension}"
                asset.MeshVars[i].Lods[j].mesh.uri = CopyFileToFolder(asset.MeshVars[i].Lods[j].mesh.uri,var_sub_folder,asset.MeshVars[i].Lods[j].mesh.name)
        asset.OriginMesh.name = asset.AssetID + asset.OriginMesh.extension
        asset.OriginMesh.uri = CopyFileToFolder(asset.OriginMesh.uri,rootFolder,asset.OriginMesh.name)
        asset.ZbrushFile = CopyFileToFolder(asset.ZbrushFile,rootFolder,f"{asset.AssetID}.ZTL")
    else:
        pass
    for i in range(len(asset.assetMaterials[0].maps)):
        asset.assetMaterials[0].maps[i].name = f"{asset.AssetID}_{asset.assetMaterials[0].maps[i].type.value}{asset.assetMaterials[0].maps[i].extension}"
        asset.assetMaterials[0].maps[i].uri = CopyFileToFolder(asset.assetMaterials[0].maps[i].uri,rootFolder,asset.assetMaterials[0].maps[i].name)
    for i in range(len(asset.previewFile)):
        asset.previewFile[i] = scaleImage(asset.previewFile[i])
        asset.previewFile[i] = CopyFileToFolder(asset.previewFile[i],rootFolder,f"{asset.AssetID}_Preview_{i}.jpg",True)
    JsonUri_abs = os.path.join(rootFolder,f"{asset.AssetID}.json")
    asset.JsonUri = os.path.basename(JsonUri_abs)
    with open(JsonUri_abs,'w+',encoding='utf-8') as f:
        f.write(json.dumps(asset.to_dict()))
    DataBaseRemote.Get().releaseDataBase()
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
        if not DataBaseRemote.Get().isAssetInDB(random_string):
            return random_string

def CopyFileToFolder(filePath:str,folder:str,newName:str = None,move:bool=False):
    if not os.path.exists(filePath):
        return ""
    newFileName = os.path.basename(filePath)
    if newName:
        newFileName = newName
    newFilePath = os.path.join(folder,newFileName)
    if move:
        shutil.move(filePath,newFilePath)
    else:
        shutil.copyfile(filePath,newFilePath)
    return os.path.basename(newFilePath)

def scaleImage(imagePath:str):
    baseName = os.path.basename(imagePath)
    name,ext = os.path.splitext(baseName)
    dirName = os.path.dirname(imagePath)

    image = readImage(imagePath)
    w,h = image.size
    image.thumbnail((512,int(512/w *h)))
    newpath = os.path.join(dirName,f"{name}_thumb{ext}")
    image.save(newpath)
    return newpath


def sendStringToUE(string:str,address:tuple[str,int]):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(address)
        client_socket.sendall(string.encode())
        client_socket.close()
        return True
    except:
        return False
    
def copyMapToFolder(map:AssetMap,folder:str)->AssetMap:
    newUri = os.path.join(folder,map.name)
    shutil.copy(map.uri,newUri)
    map.uri = newUri
    return map
def GenRoughnessMap(glossinessUri,assetID:str,dirName:str,extension:str):
    roughness_uri = os.path.join(dirName,f"{assetID}_roughness{extension}")
    if os.path.exists(roughness_uri):
        return roughness_uri
    img_gloss = readImage(glossinessUri).convert("L")
    img_roughness =Image.eval(img_gloss,lambda c: 255 - c)
    img_roughness.save(roughness_uri)
    return roughness_uri
def GenARMMap(ao:str,roughness:str,metallic:str,assetID:str,opacity:str,Translucency:str,extension:str,type:AssetType,dirName:str)->str:
    armUri = os.path.join(dirName,f"{assetID}_ARM{extension}")
    if os.path.exists(armUri):
        return armUri
    
    if roughness:
        rouImage = readImage(roughness).convert("L")
    if opacity:
        opacityImage = readImage(opacity).convert("L")
    if Translucency:
        translucencyImage = readImage(Translucency).convert("L")

    if ao:
        aoImage = readImage(ao).convert("L")
    else:
        aoImage = Image.new("L",rouImage.size,255)
    if metallic:
        metaImage = readImage(metallic).convert("L")
    else:
        metaImage = Image.new("L",rouImage.size,0)

    if type == AssetType.Assets3D or type == AssetType.Surface:
        r,g,b = aoImage.split()[0],rouImage.split()[0],metaImage.split()[0]
        armImage = Image.merge("RGB",(r,g,b))
        armImage.save(armUri)
        return armUri
    elif type == AssetType.Decal:
        r,g,b,a = aoImage.split()[0],rouImage.split()[0],metaImage.split()[0],opacityImage.split()[0]
        armImage = Image.merge("RGBA",(r,g,b,a))
        armImage.save(armUri)
        pass
    elif type == AssetType.Plant:
        r,g,b,a = aoImage.split()[0],rouImage.split()[0],translucencyImage.split()[0],opacityImage.split()[0]
        armImage = Image.merge("RGBA",(r,g,b,a))
        armImage.save(armUri)
        pass
    else:
        pass
    return armUri

def ResizeTextureByString(uri:str,rootDir:str,size:str):
    Log(f"尝试缩放贴图:{uri}")
    if not os.path.exists(rootDir):
        Log(f"尝试创建目录:{rootDir}")
        os.makedirs(rootDir)
    fileName = os.path.basename(uri)
    Log(f"贴图文件名为:{fileName}")
    newFileuri = os.path.join(rootDir,fileName)
    Log(f"缩放后贴图路径为:{newFileuri}")
    # _,ext = os.path.splitext(fileName)
    # if ext == ".exr":
    #     newFileuri = newFileuri.replace(ext,".png")
    if os.path.exists(newFileuri):
        Log(f"目录下已经存在缩放过的贴图,跳过")
        return newFileuri
    image = readImage(uri)
    if not image:
        return False
    if size == "2K":
        Log(f"将贴图缩放为2K")
        scalfactor = 2048
    elif size == "4K":
        Log(f"将贴图缩放为2K")
        scalfactor = 4096
    image = image.resize((scalfactor,scalfactor))
    image.save(newFileuri)
    Log(f"贴图缩放成功")
    return newFileuri
def fixNormalMiss(rootPath:str,asset:Asset,jsonuri:str):
    files = os.listdir(rootPath)
    files = [file for file in files if "normal" in file.lower()]
    for normal in files:
        if "lod" in normal.lower():
            index = eval(normal.lower().split("lod")[-1].split(".")[0])
            Log(f"发现存在LOD{index}的法线贴图,可以替代")
            if asset.Lods[index].normalMap.uri == "":
                asset.Lods[index].normalMap.uri = os.path.basename(normal)
                asset.Lods[index].normalMap.name,asset.Lods[index].normalMap.extension = os.path.splitext(asset.Lods[index].normalMap.uri)
        else:
            pass
    with open(jsonuri,"w",encoding='utf-8') as f:
        f.write(json.dumps(asset.to_dict()))
    return asset


def sendAssetToUE(libraryAssetData:dict,address:tuple[str,int],sizeIndex:int,lod_level:str):
    with open(libraryAssetData["jsonUri"],'r',encoding="utf-8") as f:
            asset = Asset.from_dict(json.loads(f.read()))
    rootFolder = os.path.join(Config.Get().remoteAssetLibrary,asset.rootFolder)
    
    Log(f"当前资产根目录为:{rootFolder}")
    Log(f"当前资产格式为:{asset.assetFormat.value}")
    if asset.assetFormat == AssetFormat.FBX:
        #获取所有需要的贴图
        size = list(TextureSize.__members__.values())[sizeIndex].value
        Ao = None
        Roughness = None
        BaseColor = None
        Normal = None
        Metallic = None
        Opacity = None
        Translucency = None
        Glossiness = None
        extension = ".png"
        for map in asset.assetMaterials[0].maps:
            if map.uri == "":
                continue
            mapUri = os.path.join(rootFolder,map.uri)
            if not os.path.exists(mapUri):
                continue
            if map.size.value != size:
                mapUri = ResizeTextureByString(mapUri,os.path.join(rootFolder,f"Thumbs/{size}"),size)
                if not mapUri:
                    continue
            if map.type== AssetMapType.Albedo:
                BaseColor = mapUri
            elif map.type == AssetMapType.AO:
                Ao = mapUri
            elif map.type == AssetMapType.Metalness:
                Metallic = mapUri
            elif map.type == AssetMapType.Normal:
                Normal = mapUri
            elif map.type == AssetMapType.Roughness:
                Roughness = mapUri
            elif map.type == AssetMapType.Opacity:
                Opacity = mapUri
            elif map.type == AssetMapType.Translucency:
                Translucency = mapUri
            elif map.type == AssetMapType.Gloss:
                Glossiness = mapUri
            else:
                pass
        #尝试修复法线贴图路径
        if not Normal:
            Log(f"法线贴图未找到,尝试寻找")
            asset = fixNormalMiss(rootFolder,asset,libraryAssetData["jsonUri"])
        #获取对应的mesh
        if lod_level == "original":
            meshUri = os.path.join(rootFolder,asset.OriginMesh.uri)
        else:
            lod_index = GetLodLevelByName(lod_level)
            meshUri = os.path.join(rootFolder,asset.Lods[lod_index].mesh.uri)
            if asset.Lods[lod_index].normalMap.uri != "":
                Normal = os.path.join(rootFolder,asset.Lods[lod_index].normalMap.uri)
        Log(f"当前导出的模型的地址为{meshUri}")
        #尝试寻找其他法线贴图路径
        if not Normal:
            Log(f"法线贴图仍然未找到,尝试使用其他lod的法线贴图代替")
            for lod in asset.Lods:
                Normal = os.path.join(rootFolder,lod.normalMap.uri)
                if os.path.exists(Normal):
                    break
                else:
                    Normal = None
                    Log(f"不存在其他法线贴图")

        if not Roughness and Glossiness:
            Roughness = GenRoughnessMap(Glossiness,asset.AssetID,os.path.dirname(BaseColor),extension)
        if not (Roughness and BaseColor and Normal):
            return False
        elif asset.type == AssetType.Decal and not Opacity:
            return False
        elif asset.type == AssetType.Plant and not(Opacity and Translucency):
            return False
        armUri = GenARMMap(Ao,Roughness,Metallic,asset.AssetID,Opacity,Translucency,extension,asset.type,os.path.dirname(BaseColor))
        if not armUri:
            return False
    elif asset.assetFormat == AssetFormat.UnrealEngine:
        pass

    message = dict(
        name = asset.name.replace(" ","_"),#去除资产名称中的空格
        AssetID = asset.AssetID,
        assetFormat = asset.assetFormat.value,
        assetType = asset.type.value,
        baseColor = BaseColor,
        normal = Normal,
        arm = armUri,
        mesh = meshUri
    )
    Log("将以下消息发送到UE中")
    print(message)
    if sendStringToUE(json.dumps(message),address):
        Log("消息发送成功")
        return True
    else:
        Log("消息发送失败")
        return False
def refixDB():
    path = r'\\192.168.3.126\AssetLibrary'
    dataCachePath = os.path.join(path,"AssetDataCache.json")
    assetPath = os.path.join(path,"Assets")
    db = TinyDB(dataCachePath)
    User = Query()
    for data in db.all():
        db.update({"jsonUri":os.path.basename(data["jsonUri"])},User.AssetID == data["AssetID"])
        db.update({"previewFile":os.path.basename(data["previewFile"])},User.AssetID == data["AssetID"])
        db.update({"rootFolder":data["rootFolder"].removeprefix("O:/AssetLibrary\\Assets\\")},User.AssetID == data["AssetID"])
def GetLodLevelByName(name:str)->int:
    name = name.lower()
    if "lod" not in name:
        return False
    base_name,_ = os.path.splitext(name)
    lod_level = eval(base_name.split('lod')[-1])
    return lod_level

def fixAssetData():
    path = r'\\192.168.3.126\AssetLibrary'
    dataCachePath = os.path.join(path,"AssetDataCache.json")
    assetPath = os.path.join(path,"Assets")
    db = TinyDB(dataCachePath)
    for i in range(len(db.all())):
        data = db.all()[i]
        data["rootFolder"] = os.path.join(assetPath,data["rootFolder"])
        data["previewFile"] = os.path.join(assetPath,data["rootFolder"],data["previewFile"])
        data["jsonUri"] =os.path.join(assetPath,data["rootFolder"],data["jsonUri"])
        with open(data["jsonUri"],'r',encoding="utf-8") as f:
            assetData = json.loads(f.read())
        assetData["AssetIndex"] = i
        asset = Asset.from_dict(assetData)
        asset.JsonUri = os.path.basename(asset.JsonUri)
        for i in range(len(asset.Lods)):
            asset.Lods[i].mesh.uri = os.path.basename(asset.Lods[i].mesh.uri)
            asset.Lods[i].normalMap.uri = os.path.basename(asset.Lods[i].normalMap.uri)
        asset.OriginMesh.uri = os.path.basename(asset.OriginMesh.uri)
        asset.ZbrushFile = os.path.basename(asset.ZbrushFile)
        for i in range(len(asset.assetMaterials[0].maps)):
            asset.assetMaterials[0].maps[i].uri = os.path.basename(asset.assetMaterials[0].maps[i].uri)
        asset.previewFile[0] = os.path.basename(asset.previewFile[0])
        asset.rootFolder = asset.rootFolder.split("\\")[-1]
        assetData = asset.to_dict()
        try:
            shutil.copy(data["jsonUri"],data["jsonUri"] + ".bak")
        except:
            pass
        with open(data["jsonUri"],'w+',encoding="utf-8") as f:
            f.write(json.dumps(assetData))


def checkReadAccess(path):
    return(os.access(path,os.R_OK))
def checkWriteAccess(path):
    return(os.access(path,os.W_OK) and os.access(path,os.X_OK) )

def getExeVersion(path):
    information_parser = Dispatch("Scripting.FileSystemObject")
    version = information_parser.GetFileVersion(path)
    return(version)

def compareVersion(old:str,new:str):
    oSplit = old.split(".")
    nSplit = new.split(".")
    for i in range(len(oSplit)):
        if eval(oSplit[i]) < eval(nSplit[i]):
            return True
    return False

def get_pid(pname):
    import psutil
    pids = []
    for proc in psutil.process_iter():
        if proc.name() == pname:
            pids.append(proc.pid)
    if len(pids) <= 1:
        return False
    else:
        return True

def GetExePath():
    exePath = sys.executable if getattr(sys, 'frozen', False) else __file__
    if '.exe' not in exePath:
        return False
    return exePath

def checkUpdate():
    current_exe_path = GetExePath()
    if not current_exe_path:
        return False
    currentDir = os.path.dirname(current_exe_path)
    updateExe = os.path.join(currentDir,"update.exe")
    currentVersion = getExeVersion(current_exe_path)
    #如果不存在更新exe或者本地exe直接跳过
    if not os.path.exists(current_exe_path) or not os.path.exists(updateExe):
        return False
    files = os.listdir(UPDATE_SERVE_PATH)
    #判断是否存在新版本文件
    if len(files) < 1:
        return False
    TheNewestFile = files[0]
    #获取最新的版本
    for file in files:
        if compareVersion(os.path.splitext(TheNewestFile)[0].split("_")[-1],os.path.splitext(file)[0].split("_")[-1]):
            TheNewestFile = file
    _,ext = os.path.splitext(TheNewestFile)
    if ext != ".zip":
        return False
    TheNewestFilePath = os.path.join(UPDATE_SERVE_PATH,TheNewestFile)
    DownloadedFilePath = os.path.join(currentDir,TheNewestFile)
    TheNewestFileVersion = os.path.splitext(TheNewestFile)[0].split("_")[-1]
    TempFolder = os.path.normpath(os.path.join(currentDir,"Temp"))
    if compareVersion(currentVersion,TheNewestFileVersion):
        w = Dialog("提示","有新版本,是否更新")
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        if not w.exec():
            return False
            #从服务器下载压缩包
        shutil.copyfile(TheNewestFilePath,DownloadedFilePath)
        #创建目录
        if not os.path.exists(TempFolder):
            os.makedirs(TempFolder)
        #解压文件
        with zipfile.ZipFile(DownloadedFilePath,"r") as zipRef:
            zipRef.extractall(TempFolder)
        #删除压缩文件
        os.remove(DownloadedFilePath)
        return updateExe
    return False

def AddAssetDataToDataBase(asset:Asset):
        #将资产添加到资产数据库中
        assetToLibraryData = dict(
            name        = asset.name,
            AssetID     = asset.AssetID,
            jsonUri     = asset.JsonUri,
            TilesH      = asset.TilesH,
            Tilesv      = asset.TilesV,
            asset       = asset.assetFormat.value,
            category    = asset.category,
            subcategory = asset.subcategory,
            surfaceSize = asset.surfaceSize.value,
            tags        = asset.tags,
            type        = asset.type.value,
            previewFile = asset.previewFile[0],
            rootFolder  = asset.rootFolder,
            lods        = [lod.level for lod in asset.Lods],
            SearchWords = f"{asset.name} {asset.AssetID} {asset.category} {asset.subcategory}"+" ".join(asset.tags)
            )
        while True:
            if not DataBaseRemote.Get().isRemoteDataBaseInUsed():
                DataBaseRemote.Get().UseDataBase()
                DataBaseRemote.Get().addAssetToDB(assetToLibraryData)
                DataBaseRemote.Get().releaseDataBase()
                break
            else:
                time.sleep(5)



class CustomWorker(QThread):
    onFinished = pyqtSignal()
    def __init__(self, fun,parent=None) -> None:
        super().__init__(parent)
        self.fun = fun
    def run(self) -> None:
        self.fun()
        self.onFinished.emit()





if __name__ == "__main__":
    exePath = "D:\Documents\ZCXCode\MyBridge\dist\MyBridge\MyBridge.exe"
    getExeVersion(exePath)



    

    





    
