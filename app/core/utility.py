from enum import Enum
import os
from dataclasses import dataclass,field
from collections import OrderedDict
import random
import string
import shutil
import copy
import json
from PIL import Image
import socket


from app.core.config import Config







class MyBridgetGlobalEnum(Enum):
    def __format__(self, format_spec: str) -> str:
        return super().__format__(format_spec)
class TextureSize(MyBridgetGlobalEnum):
    _2k = "2K"
    _4k = "4K"
    _8K = "8K"
class AssetType(MyBridgetGlobalEnum):
    Assets3D = "3D Assets"
    Surface = "Surface"

class Format(MyBridgetGlobalEnum):
    FBX = "Fbx"
    Unreal = "Unreal"
       
class AssetCategory(MyBridgetGlobalEnum):
    Building            =      "Building"
    Food                =      "Food"
    Historical          =      "Historical"
    Industrial          =      "Industrial"
    Interior            =      "Interior"
    Nature              =      "Nature"
    Props               =      "Props"
    Street              =      "Street"
    Aquatic             =      "Aquatic"
    Climber             =      "Climber"
    Crop                =      "Crop"
    Fern                =      "Fern"
    Flowering_Plant     =      "Flowering_Plant"
    Garden_Plant        =      "Garden_Plant"
    Grass               =      "Grass"
    Ground_Cover        =      "Ground_Cover"
    Herb                =      "Herb"
    Houseplant          =      "Houseplant"
    Shrub               =      "Shrub"
    Succulent           =      "Succulent"
    Weed                =      "Weed"
    Asphalt             =      "Asphalt"
    Bark                =      "Bark"
    Branch              =      "Branch"
    Brick               =      "Brick"
    Coal                =      "Coal"
    Concrete            =      "Concrete"
    Debris              =      "Debris"
    Fabric              =      "Fabric"
    Gravel              =      "Gravel"
    Ground              =      "Ground"
    Marble              =      "Marble"
    Metal               =      "Metal"
    Moss                =      "Moss"
    Plaster             =      "Plaster"
    Rock                =      "Rock"
    Roofing             =      "Roofing"
    Sand                =      "Sand"
    Snow                =      "Snow"
    Soil                =      "Soil"
    Stone               =      "Stone"
    Tile                =      "Tile"
    Wood                =      "Wood"
    Other               =      "Other"
    Blood               =      "Blood"
    Commercial          =      "Commercial"
    Door                =      "Door"
    Graffiti            =      "Graffiti"
    Leakage             =      "Leakage"
    Mud                 =      "Mud"
    Tree                =      "Tree"
    Trim                =      "Trim"
    Vegetation          =      "Vegetation"
    Fresh_Water         =      "Fresh_Water"
    Ocean               =      "Ocean"
    Plant               =      "Plant"
    Vine                =      "Vine"
    Damage              =      "Damage"
    Dirt                =      "Dirt"
    Fingerprint         =      "Fingerprint"
    Frost               =      "Frost"
    Grain               =      "Grain"
    Grunge              =      "Grunge"
    Rubber              =      "Rubber"
    Stain               =      "Stain"
    Wipe_Mark           =      "Wipe_Mark"
    Imprint             =      "Imprint"
    Scorch_Mark         =      "Scorch_Mark"
    Spatter             =      "Spatter"
    Sponge              =      "Sponge"
    Traditional         =      "Traditional"


class AssetSubccategory(MyBridgetGlobalEnum):
    Balcony = "Balcony"
    Beam    = "Beam"
    Combined = "Combined"
    Door = "Door"
    Pillar = "Pillar"
    Railing = "Railing"
    Relief = "Relief"
    Roof = "Roof"
    Roof_Tile = "Roof_Tile"
    Stair = "Stair"
    Trim = "Trim"
    Wall = "Wall"
    Window = "Window"
    Baked_Goods = "Baked_Goods"
    Fruit = "Fruit"
    Meat = "Meat"
    Mushroom = "Mushroom"
    Nut = "Nut"
    Vegetable = "Vegetable"
    Cambodian_Ruins = "Cambodian_Ruins"
    Feudal_Japan = "Feudal_Japan"
    Medieval = "Medieval"
    Roman_Empire = "Roman_Empire"
    Wild_West = "Wild_West"
    Construction = "Construction"
    Hardware = "Hardware"
    Mining = "Mining"
    Railway = "Railway"
    Storage = "Storage"
    Ceiling = "Ceiling"
    Decoration = "Decoration"
    Fireplace = "Fireplace"
    Furniture = "Furniture"
    Bone = "Bone"
    Debris = "Debris"
    Embankment = "Embankment"
    Rock = "Rock"
    Seabed = "Seabed"
    Snow = "Snow"
    Tree = "Tree"
    Books = "Books"
    Farm = "Farm"
    Firewood = "Firewood"
    Military = "Military"
    Palisade = "Palisade"
    Recreational = "Recreational"
    Trash = "Trash"
    Weaponry = "Weaponry"
    Wheel = "Wheel"
    Wood = "Wood"
    Barrier = "Barrier"
    Bollard = "Bollard"
    Curb = "Curb"
    Highway = "Highway"
    Props = "Props"
    Sidewalk = "Sidewalk"
    Traffic_Cone = "Traffic_Cone"
    Floating = "Floating"
    Shore = "Shore"
    Submerged = "Submerged"
    Grass = "Grass"
    Plant = "Plant"
    Flowerhead = "Flowerhead"
    Infloresence = "Infloresence"
    Bush = "Bush"
    Flowering = "Flowering"
    Flowerless = "Flowerless"
    Lawn = "Lawn"
    Wild = "Wild"
    Forest = "Forest"
    Meadow = "Meadow"
    Sandy = "Sandy"
    Urban = "Urban"
    Fine = "Fine"
    Rough = "Rough"
    Torn = "Torn"
    Beech = "Beech"
    Birch = "Birch"
    Oak = "Oak"
    Other = "Other"
    Plam = "Plam"
    Pine = "Pine"
    Spruce = "Spruce"
    Willow = "Willow"
    Alder = "Alder"
    Juniper = "Juniper"
    Modern = "Modern"
    Mortar = "Mortar"
    Painted = "Painted"
    Brick = "Brick"
    Cast_in_Situ = "Cast_in_Situ"
    Damaged = "Damaged"
    Dirty = "Dirty"
    Slab = "Slab"
    Smooth = "Smooth"
    Nature = "Nature"
    Carpet = "Carpet"
    Leather = "Leather"
    Pattern = "Pattern"
    Plain = "Plain"
    Tarp = "Tarp"
    Artificial = "Artificial"
    Dried = "Dried"
    Patchy = "Patchy"
    Natural = "Natural"
    Pebbledash = "Pebbledash"
    Jungle = "Jungle"
    Roots = "Roots"
    Asian = "Asian"
    Middle_Eastern = "Middle_Eastern"
    Roman = "Roman"
    Polished = "Polished"
    Tile = "Tile"
    Bare = "Bare"
    Corroded = "Corroded"
    Corrugated = "Corrugated"
    Gun = "Gun"
    Sheet = "Sheet"
    Treated = "Treated"
    Ground = "Ground"
    Fresh = "Fresh"
    Old = "Old"
    Cliff = "Cliff"
    Jagged = "Jagged"
    Lava = "Lava"
    Mossy = "Mossy"
    New = "New"
    Beach = "Beach"
    Desert = "Desert"
    Mixed = "Mixed"
    Pure = "Pure"
    Clay = "Clay"
    Mud = "Mud"
    Mulch = "Mulch"
    Castle = "Castle"
    Cobblestone = "Cobblestone"
    Floor = "Floor"
    Granite = "Granite"
    Limestone = "Limestone"
    Mosaic = "Mosaic"
    Pebble = "Pebble"
    Terrazzo = "Terrazzo"
    Ceramic = "Ceramic"
    Grout = "Grout"
    Pavestone = "Pavestone"
    Stone = "Stone"
    Board = "Board"
    Log = "Log"
    Parquet = "Parquet"
    Plank = "Plank"
    Veneer = "Veneer"
    Climber = "Climber"
    Creature = "Creature"
    Dirt_Road = "Dirt_Road"
    Edible = "Edible"
    Fur = "Fur"
    Paper = "Paper"
    Various = "Various"
    Spatter = "Spatter"
    Stain = "Stain"
    Poster = "Poster"
    Sticker = "Sticker"
    Crack = "Crack"
    Damage = "Damage"
    Patch = "Patch"
    Ash = "Ash"
    Burnt = "Burnt"
    Dirt = "Dirt"
    Metal = "Metal"
    Rag = "Rag"
    Rug = "Rug"
    Stamp = "Stamp"
    Tileable = "Tileable"
    Manhole_Cover = "Manhole_Cover"
    Scrap = "Scrap"
    Welding_Seam = "Welding_Seam"
    Spanish = "Spanish"
    Antique = "Antique"
    Painted_line = "Painted_line"
    Porhole = "Porhole"
    Bark = "Bark"
    Branch = "Branch"
    Flower = "Flower"
    Hay = "Hay"
    Leaf = "Leaf"
    Twig = "Twig"
    Vine = "Vine"
    Weed = "Weed"
    Belt = "Belt"
    Table_Mat = "Table_Mat"
    Stem = "Stem"
    Needle = "Needle"
    Assorted_Plant = "Assorted_Plant"
    Painting = "Painting"
    Clean = "Clean"
    Scratched     = "Scratched"


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

    type           : AssetType         = field(default=AssetType.Assets3D)
    category       : AssetCategory     = field(default=AssetCategory.Building)
    subcategory    : AssetSubccategory = field(default=AssetSubccategory.Floating)
    surfaceSize    : AssetSize        = field(default=AssetSize.Meter1)
    assetFormat    : AssetFormat       = field(default=AssetFormat.FBX)

    OriginMesh     : AssetMesh         = field(default_factory=AssetMesh)


    TilesV         : bool              = field(default_factory=bool)
    TilesH         : bool              = field(default_factory=bool)

    AssetIndex     : int               = field(default_factory=int)

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
def GetTextureSize(uri:str):
    image = Image.open(uri)
    size = image.size
    maxSize = max(size[0],size[1])
    if maxSize >= 8192:
        return TextureSize._8K
    elif maxSize >= 4096:
        return TextureSize._4k
    else:
        return TextureSize._2k
def MakeAssetByData(datas:dict)->Asset:
    asset = Asset()
    asset.name = datas["name"]
    asset.tags = [tag for tag in datas["tags"].split(",")]
    asset.type = copy.deepcopy(AssetType._value2member_map_[datas["type"]])
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
    asset.assetFormat = AssetFormat.FBX
    return CopyAndRenameAsset(asset)

def CopyAndRenameAsset(asset:Asset):
    # 计算资产ID
    asset.AssetID = generate_unique_string(7)
    # 创建资产根目录
    asset.rootFolder = os.path.join(Config.Get().remoteAssetLibrary,f"{asset.name}_{asset.AssetID}")
    if not os.path.exists(asset.rootFolder):
        os.makedirs(asset.rootFolder)
    # 获取资产编号
    asset.AssetIndex = Config.Get().getCurrentAssetCount()

    asset.JsonUri = os.path.join(asset.rootFolder,f"{asset.AssetID}.json")

    if asset.type == AssetType.Assets3D:
        for i in range(len(asset.Lods)):
            asset.Lods[i].mesh.name = f"{asset.AssetID}_LOD{asset.Lods[i].level}{asset.Lods[i].mesh.extension}"
            asset.Lods[i].mesh.uri = CopyFileToFolder(asset.Lods[i].mesh.uri,asset.rootFolder,asset.Lods[i].mesh.name)
            asset.Lods[i].normalMap.name = f"{asset.AssetID}_Normal_LOD{asset.Lods[i].level}{asset.Lods[i].normalMap.extension}"
            asset.Lods[i].normalMap.uri = CopyFileToFolder(asset.Lods[i].normalMap.uri,asset.rootFolder,asset.Lods[i].normalMap.name)
        asset.OriginMesh.name = asset.AssetID + asset.OriginMesh.extension
        asset.OriginMesh.uri = CopyFileToFolder(asset.OriginMesh.uri,asset.rootFolder,asset.OriginMesh.name)
        asset.ZbrushFile = CopyFileToFolder(asset.ZbrushFile,asset.rootFolder,f"{asset.AssetID}.ZTL")
    else:
        pass
    for i in range(len(asset.assetMaterials[0].maps)):
        asset.assetMaterials[0].maps[i].name = f"{asset.AssetID}_{asset.assetMaterials[0].maps[i].type.value}{asset.assetMaterials[0].maps[i].extension}"
        asset.assetMaterials[0].maps[i].uri = CopyFileToFolder(asset.assetMaterials[0].maps[i].uri,asset.rootFolder,asset.assetMaterials[0].maps[i].name)
    for i in range(len(asset.previewFile)):
        asset.previewFile[i] = scaleImage(asset.previewFile[i])
        asset.previewFile[i] = MoveFileToFolder(asset.previewFile[i],asset.rootFolder,f"{asset.AssetID}_Preview_{i}.jpg")
    with open(asset.JsonUri,'w+',encoding='utf-8') as f:
        f.write(json.dumps(asset.to_dict()))
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
def MoveFileToFolder(filePath:str,folder:str,newName:str = None):
    newFileName = os.path.basename(filePath)
    if newName:
        newFileName = newName
    newFilePath = os.path.join(folder,newFileName)
    shutil.move(filePath,newFilePath)
    return newFilePath
def scaleImage(imagePath:str):
    baseName = os.path.basename(imagePath)
    name,ext = os.path.splitext(baseName)
    dirName = os.path.dirname(imagePath)

    image = Image.open(imagePath)
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

def GenARMMap(ao:str,roughness:str,metallic:str,assetID:str,extension:str)->str:
    dirName = os.path.dirname(ao)
    armUri = os.path.join(dirName,f"{assetID}_ARM{extension}")
    if os.path.exists(armUri):
        return armUri
    aoImage = Image.open(ao).convert("L")
    rouImage = Image.open(roughness).convert("L")
    metaImage = Image.open(metallic).convert("L")
    assert aoImage.size == rouImage.size == metaImage.size
    r,g,b = aoImage.split()[0],rouImage.split()[0],metaImage.split()[0]
    armImage = Image.merge("RGB",(r,g,b))
    armImage.save(armUri)
    return armUri
def ResizeTextureByString(uri:str,rootDir:str,size:str):
    if not os.path.exists(rootDir):
        os.makedirs(rootDir)
    fileName = os.path.basename(uri)
    newFileuri = os.path.join(rootDir,fileName)
    if os.path.exists(newFileuri):
        return newFileuri
    if size == "2K":
        image = Image.open(uri)
        image = image.resize((2048,2048))
        image.save(newFileuri)
        return newFileuri
    elif size == "4K":
        image = Image.open(uri)
        image = image.resize((4096,4096))
        image.save(newFileuri)
        return newFileuri
    return uri
def sendAssetToUE(libraryAssetData:dict,address:tuple[str,int],sizeIndex:int):
    with open(libraryAssetData["jsonUri"],'r',encoding="utf-8") as f:
            asset = Asset.from_dict(json.loads(f.read()))
    if asset.assetFormat == AssetFormat.FBX:
        size = list(TextureSize.__members__.values())[sizeIndex].value
        meshUri = asset.OriginMesh.uri
        Ao = None
        Roughness = None
        BaseColor = None
        Normal = None
        Metallic = None
        extension = ".png"
        for map in asset.assetMaterials[0].maps:
            mapUri = map.uri
            if map.size.value != size:
                mapUri = ResizeTextureByString(mapUri,os.path.join(asset.rootFolder,f"Thumbs/{size}"),size)
            if map.type== AssetMapType.Albedo:
                BaseColor = mapUri
                extension = map.extension
            elif map.type == AssetMapType.AO:
                Ao = mapUri
            elif map.type == AssetMapType.Metalness:
                Metallic = mapUri
            elif map.type == AssetMapType.Normal:
                Normal = mapUri
            elif map.type == AssetMapType.Roughness:
                Roughness = mapUri
            else:
                pass
        if not (Ao and Roughness and BaseColor and Normal and Metallic):
            return
        armUri = GenARMMap(Ao,Roughness,Metallic,asset.AssetID,extension)
    elif asset.assetFormat == AssetFormat.UnrealEngine:
        pass
    message = dict(
        name = asset.name,
        AssetID = asset.AssetID,
        assetFormat = asset.assetFormat.value,
        assetType = asset.type.value,
        baseColor = BaseColor,
        normal = Normal,
        arm = armUri,
        mesh = meshUri
    )
    if sendStringToUE(json.dumps(message),address):
        return True
    else:
        return False
if __name__ == "__main__":
    print(ClassifyFilesFormFolder("d:\Desktop\Temp\Bmwl_1"))

    





    
