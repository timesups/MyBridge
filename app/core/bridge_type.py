
import utility as utility
import os
import json

from dataclasses import field



path = r'O:\Shade\Quixel_Textures\Downloaded\3d\3d_Building_vcknaa3dw'




def json_load(json_data,path):

    asset_data = utility.Asset()

    asset_data.name             = json_data["name"]
    asset_data.ZbrushFile       = field(default_factory=str)
    asset_data.AssetID          = field(default_factory=str)
    asset_data.rootFolder       = path
    asset_data.JsonUri          = field(default_factory=str)

    asset_data.tags             = json_data["tags"]
    asset_data.previewFile      = folderTraversal(path,'previews')
    asset_data.Lods             = lodDataProcess(path,json_data)
    asset_data.assetMaterials   = assetMaterialsProcess(path,json_data)

    asset_data.type             = utility.AssetType.Assets3D
    asset_data.category         = categoryProcess(json_data)
    asset_data.subcategory      = subcategoryProcess(json_data)
    asset_data.surfaceSize      = utility.AssetSize.Meter1
    asset_data.assetFormat      = utility.AssetFormat.FBX

    asset_data.OriginMesh       = utility.AssetMesh

    asset_data.TilesV           = False
    asset_data.TilesH           = False

    asset_data.AssetIndex       = field(default_factory=int)

    return asset_data

    

def originMeshProcess(path,json_data):
    
    #获取high模型uri
    try:
        try:
            mesh_uri = json_data["meshes"][0]["uris"][1]["uri"]
        except:
            mesh_uri = json_data["models"][0]["uri"]
    except:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if '_High' in filename:
                    mesh_uri = filename
                    break
                elif '_LOD0.' in filename:
                    mesh_uri = filename
    
    
    #输入模型信息
    mesh = utility.AssetMesh()
    mesh.uri = path+'\\'+mesh_uri
    mesh.name = mesh_uri
    mesh.extension = '.fbx'

    return mesh
    

def subcategoryProcess(json_data):
    subcategorie = ''
    #获取categorie
    categories = json_data["assetCategories"]['3D asset']
    for categories_key,categories_value in categories.items():
        for subcategories_key,subcategories_value in categories_value.items():
            subcategorie = subcategories_key
            break
    
    #获取subcategorie
    subcategories_type = utility.AssetSubccategory.__members__ 
    #遍历枚举信息   
    for name, member in subcategories_type.items():
        #比较内容
        if subcategorie == name .lower():
            subcategorie = eval(f"utility.AssetSubccategory.{name}")
            break

    return subcategorie

    

def categoryProcess(json_data):
    categorie = ''
    #获取categorie
    categories = json_data["assetCategories"]['3D asset']
    for categories_key,categories_value in categories.items():
        categorie = categories_key
    
    categories_type = utility.AssetCategory.__members__
    for name, member in categories_type.items():
        #比较内容
        if categorie == name.lower():
            categorie = eval(f"utility.AssetCategory.{name}")
            break
    

    return categorie
    


def assetMaterialsProcess(path,json_data):
    map_types=["Albedo","AO","Cavity","Displacement","Gloss","Metalness","Normal","Roughness","Specular","Bump","Brush","Diffuse","Fuzz","Mask","Opacity","Translucency"]
    materials = []
    maps = []
    material_data = utility.Material()
    #赋予名称
    material_data.name = json_data["name"]
    try:
        components=json_data["components"]
        #遍历components
        for component in components:
            #遍历贴图类型
            for map_type in map_types:
                #比较贴图类型是否匹配
                if component["type"] == map_type.lower():
                    map_uris = component["uris"][0]["resolutions"][0]["formats"]
                    #判断贴图格式类型
                    if map_uris[1]["mimeType"] == "image/jpeg":
                        #创建AssetMap类
                        asset_map = utility.AssetMap()
                        asset_map.uri = path+'\\'+map_uris[1]["uri"]
                        asset_map.extension = ".jpg"
                        asset_map.name = map_uris[1]["uri"]
                        asset_map.type = eval(f"utility.AssetMapType.{map_type}")
                        asset_map.subMapCount = 1
                        if len(map_uris[1]["uri"].split('.'))>2:
                            asset_map.UDIM = True
                        else:
                            asset_map.UDIM = False
                        if '_8K_' in asset_map.uri:
                            asset_map.size = utility.TextureSize._8K
                        elif '_4K_' in asset_map.uri:
                            asset_map.size = utility.TextureSize._4k
                        elif '_2K_' in asset_map.uri:
                            asset_map.size = utility.TextureSize._2k

                        maps.append(asset_map)
    except:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                for map_type in map_types:
                    if 'K_'+map_type+'.' in filename and '.jpg' in filename:
                        asset_map = utility.AssetMap()
                        asset_map.uri = dirpath+'\\'+filename
                        asset_map.extension = ".jpg"
                        asset_map.name = filename
                        asset_map.type = eval(f"utility.AssetMapType.{map_type}")
                        asset_map.subMapCount = 1
                        if len(filename.split('.'))>2:
                            asset_map.UDIM = True
                        else:
                            asset_map.UDIM = False
                        if '_8K_' in asset_map.uri:
                            asset_map.size = utility.TextureSize._8K
                        elif '_4K_' in asset_map.uri:
                            asset_map.size = utility.TextureSize._4k
                        elif '_2K_' in asset_map.uri:
                            asset_map.size = utility.TextureSize._2k

                        maps.append(asset_map)

    material_data.maps = maps
    materials.append(material_data)
    return materials
    

def lodDataProcess(path,json_data):
    lod_datas = []
    try:
        meshes=json_data["meshes"]
        uri_type = "meshes"
    except:
        meshes=json_data["models"]
        uri_type = "models"
    for mesh in meshes:
        if mesh["type"] == "lod":
            lod_data = utility.LOD()
            if uri_type == "meshes":
                lod_model = mesh["uris"][1]["uri"]
            elif uri_type == "models":
                lod_model = mesh["uri"]
            if '.fbx' in lod_model:
                    asset_mesh=utility.AssetMesh()
                    #获取lod的uri
                    asset_mesh.uri = lod_model
                    #获取fbx名称
                    asset_mesh.name = lod_model.split('.fbx')[0]
                    #设置后缀名
                    asset_mesh.extension = '.fbx'
                    lod_data.mesh = asset_mesh
                    lod_num = lod_model.split('.fbx')[0].rsplit('_LOD')[1]
                    lod_data.level = int(lod_num)
                    lod_datas.append(lod_data)

    # #遍历components
    # components=json_data["components"]
    # for component in components:
    #     #判断贴图类型是否为normal
    #     if component["type"] == "normal":
    #         #获取所有法线贴图信息
    #         normal_uris = component["uris"][0]["resolutions"][0]["formats"]
    #         #遍历法线信息
    #         for normal_uri in normal_uris:
    #             if normal_uri["mimeType"] == "image/jpeg":


    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if 'normal_lod' in filename.lower():
                #创建AssetMap类
                asset_normal_map = utility.AssetMap()
                asset_normal_map.uri = dirpath+'\\'+filename
                asset_normal_map.extension = ".jpg"
                asset_normal_map.name = filename
                asset_normal_map.type = utility.AssetMapType.Normal
                asset_normal_map.subMapCount = 1
                #判断是否为UDIM贴图
                if len(filename.split('.'))>2:
                    asset_normal_map.UDIM = True
                else:
                    asset_normal_map.UDIM = False
                if '_8K_' in asset_normal_map.uri:
                    asset_normal_map.size = utility.TextureSize._8K
                elif '_4K_' in asset_normal_map.uri:
                    asset_normal_map.size = utility.TextureSize._4k
                elif '_2K_' in asset_normal_map.uri:
                    asset_normal_map.size = utility.TextureSize._2k
                for lod_data in lod_datas :
                    lod_data:utility.LOD
                    #比较法线贴图与LOD的命名,相同则写入到LOD信息
                    if lod_data.mesh.name.split('.fbx')[0].split('_')[-1] in asset_normal_map.name:
                        lod_data.normalMap = asset_normal_map
                    
    return lod_datas

        
#根据文件夹名称获取文件
def folderTraversal(path,folder_name):
    folder_name=path+'\\'+folder_name
    flie_paths=[]
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if folder_name == dirpath:
                    file_path = dirpath+'\\'+filename
                    flie_paths.append(file_path)
    return flie_paths
     



def bridgeToAsset(path):
    #遍历文件夹内文件
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if '.json' in filename.lower():
                json_path = dirpath+'\\'+filename
                root_path = dirpath
                with open(json_path,'r') as js_file:
                    try:
                        json_data=json.load(js_file)
                        asset_data = json_load(json_data,root_path)
                        print(asset_data.name)
                        return asset_data
                    except:
                        return False
    





if __name__ == "__main__":
    bridgeToAsset(path)

