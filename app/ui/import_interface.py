# coding: utf-8
from qfluentwidgets import (PushButton,SmoothScrollArea,ComboBox,
                            TitleLabel,CheckBox,LineEdit,
                            LineEditButton,IndeterminateProgressRing,
                            InfoBar,InfoBarPosition,FlowLayout,Dialog)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import (QApplication,QWidget,
                             QHBoxLayout,QVBoxLayout,
                             QLabel,QLineEdit,QTabWidget,
                             QFileDialog,QTabBar,QSizePolicy)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent,QPalette)
from PyQt5.QtCore import QObject, QSize,pyqtSignal
from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve,QThread
import time
import os


from app.core.utility import AssetCategory,AssetSize,AssetSubccategory,AssetType,ClassifyFilesFormFolder,MakeAndCopyAsset
import app.core.utility as ut
from app.core.style_sheet import StyleSheet
from app.core.translator import Translator
from app.core.config import Config
from app.core.datebase import DataBaseRemote
from app.core.common_widgets import scaleMap
import app.core.common_widgets as common
from app.core.Log import Log

class SelectFileLineEdit(LineEdit):
    selectedFile = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.openBrowserButton = LineEditButton(FIF.FOLDER, self)
        self.openBrowserButton.setIconSize(QSize(self.openBrowserButton.width()-4,self.openBrowserButton.width()-4))
        self.hBoxLayout.addWidget(self.openBrowserButton, 0, Qt.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)
        self.title = "select a file"
        self.filter = "All Files(*)"
        self.rootPath = "."
        self.__initConnection()
    def __initConnection(self):
        self.openBrowserButton.clicked.connect(self.selectFile)
        pass
    def selectFile(self):
        options = QFileDialog.Options()
        fileUrl,_ = QFileDialog.getOpenFileName(self,self.title,filter=self.filter,options=options,directory=self.rootPath)
        if fileUrl != "":
            self.setText(fileUrl)
            self.selectedFile.emit()
    def setTitle(self,title:str):
        self.title = title
    def setFilter(self,filter:str):
        self.filter = filter
    def setRootPath(self,path:str):
        self.rootPath = path
 
class DirectiorySelectGroup(QWidget):
    textChanged = pyqtSignal(str)
    def __init__(self, parent,text:str,textMaxWidth:int = 50,title:str="选择一个文件",filter:str = "All Files(*)",rootPath:str="."):
        super().__init__(parent)
        self.texMaxWidth = textMaxWidth
        self.rootLayout = QHBoxLayout(self)
        self.label = QLabel(self,text=text)
        self.checkbox = CheckBox(self)
        self.lineEdit = SelectFileLineEdit(self)
        self.lineEdit.setTitle(title)
        self.lineEdit.setFilter(filter)
        self.lineEdit.setRootPath(rootPath)
        self.__initWidget()
        self.__initConnections()
        self.GroupLabel = text.lower()
    def __initWidget(self):
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.addWidget(self.checkbox)
        self.rootLayout.addWidget(self.label)
        self.rootLayout.addWidget(self.lineEdit)
        self.label.setFixedWidth(self.texMaxWidth-15)
        self.checkbox.setFixedWidth(15)
    def __initConnections(self):
        self.lineEdit.selectedFile.connect(lambda: self.checkbox.setChecked(True))
        self.lineEdit.textChanged.connect(lambda: self.textChanged.emit(self.lineEdit.text()))
        self.checkbox.stateChanged.connect(self.selectFile)
        pass
    def selectFile(self):
        if self.checkbox.isChecked() and self.lineEdit.text() == "":
            self.lineEdit.selectFile()
class TagButton(PushButton):
    index = 0
    deletClicked = pyqtSignal(int)
    def __init__(self,text,icon,parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setIcon(icon)
        self.clicked.connect(lambda:self.deletClicked.emit(self.index))
    pass
class LineEidtGroup(QWidget):

    def __init__(self, parent,text:str,textMaxWidth:int = 50):
        super().__init__(parent)
        self.textMaxWidth = textMaxWidth

        self.rootLayout = QHBoxLayout(self)
        self.labelText =QLabel(self,text=text)
        self.lineEdit = LineEdit(self)
        self.__initWidget()
        self.__initConnections()
    def __initWidget(self):
        self.rootLayout.addWidget(self.labelText)
        self.rootLayout.addWidget(self.lineEdit)
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.labelText.setFixedWidth(self.textMaxWidth)
    def __initConnections(self):

        pass

class ComboxGroup(QWidget):
    def __init__(self, parent,text:str,textMaxWidth:int = 50):
        super().__init__(parent)
        self.textMaxWidth = textMaxWidth
        self.rootLayout = QHBoxLayout(self)
        self.labelText =QLabel(self,text=text)
        self.combox = ComboBox(self)
        self.__initWidget()
    def __initWidget(self):
        self.rootLayout.addWidget(self.labelText)
        self.rootLayout.addWidget(self.combox)
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.labelText.setFixedWidth(self.textMaxWidth)
    def addItems(self,items:list[str]):
        self.combox.addItems(items)

class TabBarButton(QWidget):
    clicked = pyqtSignal(int)
    delete_clicked = pyqtSignal(int)
    def __init__(self, parent,text:str,index:int):
        super().__init__(parent)
        self.rootLayout = QHBoxLayout(self)
        self.selectedFlageWidth = 5
        self.setFixedSize(200, 25)
        self.label = QLabel(self,text=text)
        self.isSelected = False
        self.button_delete = PushButton(self)
        self.index = index

        self.__initWidget()
        self.__initConnection()
    def __initWidget(self):

        self.rootLayout.addWidget(self.label)
        self.rootLayout.addWidget(self.button_delete)
        self.rootLayout.setContentsMargins(self.selectedFlageWidth+10,0,30,0)


        self.button_delete.setFixedSize(self.height()-2,self.height()-2)
        pass
    def __initConnection(self):
        self.button_delete.clicked.connect(lambda :self.delete_clicked.emit(self.index))
    def paintEvent(self, a0: QPaintEvent | None) -> None:
        super().paintEvent(a0) 
        if not self.isSelected:
            return
        painter = QPainter(self)
        rect = QRect(0,0,self.selectedFlageWidth,self.height())
        painter.fillRect(rect,QColor(139,194,74,255))
        painter.end()
    def setSelected(self,isSelected:bool,force=False):
        if isSelected == self.isSelected and not force:
            return
        self.isSelected = isSelected
        self.setProperty("isSelected",self.isSelected)
        self.setStyle(QApplication.style())
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if self.isSelected:
            return
        self.clicked.emit(self.index)
    def setText(self,text:str):
        self.label.setText(text)

class MakeAssetWorker(QThread):
    onFinished = pyqtSignal()
    onRemoteDatabaseIsUsed = pyqtSignal()
    onRemoteDatabaseIsUsedCountDone = pyqtSignal()
    def __init__(self, assetData,parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.assetdata = assetData
    def run(self) -> None:
        asset = MakeAndCopyAsset(self.assetdata)
        #将资产添加到资产数据库中
        assetToLibraryData = dict(
            name        = asset.name,
            AssetID     = asset.AssetID,
            jsonUri     = asset.JsonUri,
            TilesH      = asset.TilesH,
            Tilesv      = asset.TilesV,
            asset       = asset.assetFormat.value,
            category    = asset.category.value,
            subcategory = asset.subcategory.value,
            surfaceSize = asset.surfaceSize.value,
            tags        = asset.tags,
            type        = asset.type.value,
            previewFile = asset.previewFile[0],
            rootFolder  = asset.rootFolder,
            )
        while True:
            if not DataBaseRemote.Get().isRemoteDataBaseInUsed():
                DataBaseRemote.Get().UseDataBase()
                DataBaseRemote.Get().addAssetToDB(assetToLibraryData)
                DataBaseRemote.Get().releaseDataBase()
                self.onFinished.emit()
                break
            else:
                self.onRemoteDatabaseIsUsed.emit()
                time.sleep(5)
                self.onRemoteDatabaseIsUsedCountDone.emit()

class ImportSettings(QWidget,Translator):
    startImported = pyqtSignal()
    endImported = pyqtSignal(int)
    def __init__(self, parent,index:int,rootpath:str = "."):
        super().__init__(parent)
        self.index = index
        #value
        self.maxTextWidth = 150
        self.texFilter = "图像(*.jpg *.png *.exr)"
        self.lods:list[DirectiorySelectGroup] = []
        self.rootPath = rootpath
        #widget
        self.rootLayout = QVBoxLayout(self)

        self.scrollArea = SmoothScrollArea(self)
        self.scrollWidget = QWidget(self)
        self.scrollWidgetLayout = QVBoxLayout(self.scrollWidget)


        self.label_nameTga = TitleLabel(self.tra("Import Settings"),self)
        self.leg_name = LineEidtGroup(self,self.tra("Name"),self.maxTextWidth)

        self.tags_widegt = QWidget(self)
        self.tags_widegt.setMinimumHeight(30)

        self.tags_flowLayout = FlowLayout(self.tags_widegt,False)

        self.tags_flowLayout .setContentsMargins(10,10,10,10)
        self.tags_flowLayout .setVerticalSpacing(20)
        self.tags_flowLayout .setHorizontalSpacing(10)



        self.tags = []
        self.leg_tags = LineEidtGroup(self,self.tra("Tags"),self.maxTextWidth)
        
        self.combox_type = ComboxGroup(self,self.tra("Type"),self.maxTextWidth)

        self.widgetCategorys = QWidget(self)
        self.widgetCategorysLayout = QHBoxLayout(self.widgetCategorys)

        self.combox_category = ComboxGroup(self.widgetCategorys,self.tra("Category"),self.maxTextWidth)
        self.combox_subcategory = ComboxGroup(self.widgetCategorys,self.tra("Subcategory"),self.maxTextWidth)

        self.widgetSize = QWidget(self)
        self.widgetSizeLayout = QHBoxLayout(self.widgetSize)

        
        self.combox_SurfaceSize = ComboxGroup(self.widgetSize,self.tra("Surface Size"),self.maxTextWidth)
        self.checkbox_TilesVertically = CheckBox(self.tra("Tiles Vertically"),self.widgetSize)
        self.checkbox_TilesVertically.setChecked(True)
        self.checkobx_TillesHorizontically = CheckBox(self.tra("Tiles Horizontically"),self.widgetSize)
        self.checkobx_TillesHorizontically.setChecked(True)


        self.group_texAlbedo = DirectiorySelectGroup(self,self.tra("Albedo"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texbrush = DirectiorySelectGroup(self,self.tra("Brush"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texAO = DirectiorySelectGroup(self,self.tra("AO"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texBump = DirectiorySelectGroup(self,self.tra("Bump"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texCavity= DirectiorySelectGroup(self,self.tra("Cavity"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texDiffuse = DirectiorySelectGroup(self,self.tra("Diffuse"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texDisplacement = DirectiorySelectGroup(self,self.tra("Displacement"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texFuzz = DirectiorySelectGroup(self,self.tra("Fuzz"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texGloss = DirectiorySelectGroup(self,self.tra("Gloss"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texMask = DirectiorySelectGroup(self,self.tra("Mask"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texMetalness = DirectiorySelectGroup(self,self.tra("Metalness"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texNormal = DirectiorySelectGroup(self,self.tra("Normal"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texOpacity = DirectiorySelectGroup(self,self.tra("Opacity"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texRoughness = DirectiorySelectGroup(self,self.tra("Roughness"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texSpecular = DirectiorySelectGroup(self,self.tra("Specular"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texTranslucency = DirectiorySelectGroup(self,self.tra("Translucency"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)

        self.textureGroups = [
                                self.group_texAlbedo,
                                self.group_texbrush,
                                self.group_texAO,
                                self.group_texBump,
                                self.group_texCavity,
                                self.group_texDiffuse,
                                self.group_texDisplacement ,
                                self.group_texFuzz,
                                self.group_texGloss,
                                self.group_texMask,
                                self.group_texMetalness,
                                self.group_texNormal ,
                                self.group_texOpacity ,
                                self.group_texRoughness,
                                self.group_texSpecular ,
                                self.group_texTranslucency ,]

        self.OriginMesh =  DirectiorySelectGroup(self,self.tra(f"Mesh"),self.maxTextWidth,title="选择一个模型",filter="fbx file(*.fbx)",rootPath=self.rootPath)

        self.lodWidget = QWidget(self.scrollWidget)
        self.lodWidgetLayout = QVBoxLayout(self.lodWidget)
        self.button_addlod = PushButton("add lod Mesh",self.scrollWidget)
        
        self.group_previewImage = DirectiorySelectGroup(self,self.tra("Preview Image"),self.maxTextWidth,filter="all files(*)",rootPath=self.rootPath)

        self.ImagePreview = QLabel(self)


        self.button_importAsset = PushButton("Import",self)
        
        self.__initWidget()
        self.__initConnection()
    def __initWidget(self):
        self.rootLayout.addWidget(self.scrollArea)
        self.rootLayout.setContentsMargins(0,0,0,0)
        



        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0,0,0,0)
        self.scrollArea.setObjectName("ImportSettingsScrollArea")


        self.scrollWidget.setObjectName("ScrollWidget")




        self.scrollWidgetLayout.addWidget(self.label_nameTga)
        self.scrollWidgetLayout.addWidget(self.leg_name)
        self.scrollWidgetLayout.addWidget(self.tags_widegt)
        self.scrollWidgetLayout.addWidget(self.leg_tags)

        self.leg_tags.lineEdit.returnPressed.connect(self.addTag)

        self.scrollWidgetLayout.addWidget(common.QLine.HLine(self))

        self.scrollWidgetLayout.addWidget(self.combox_type)
        self.scrollWidgetLayout.addWidget(self.widgetCategorys)
        self.scrollWidgetLayout.addWidget(self.widgetSize)

        self.scrollWidgetLayout.addWidget(common.QLine.HLine(self))

        self.scrollWidgetLayout.addWidget(self.group_texAlbedo)
        self.scrollWidgetLayout.addWidget(self.group_texAO)
        self.scrollWidgetLayout.addWidget(self.group_texbrush)
        self.scrollWidgetLayout.addWidget(self.group_texBump)
        self.scrollWidgetLayout.addWidget(self.group_texCavity)
        self.scrollWidgetLayout.addWidget(self.group_texDiffuse)
        self.scrollWidgetLayout.addWidget(self.group_texDisplacement)
        self.scrollWidgetLayout.addWidget(self.group_texFuzz)
        self.scrollWidgetLayout.addWidget(self.group_texGloss)
        self.scrollWidgetLayout.addWidget(self.group_texMask)
        self.scrollWidgetLayout.addWidget(self.group_texMetalness)
        self.scrollWidgetLayout.addWidget(self.group_texNormal)
        self.scrollWidgetLayout.addWidget(self.group_texOpacity)
        self.scrollWidgetLayout.addWidget(self.group_texRoughness)
        self.scrollWidgetLayout.addWidget(self.group_texSpecular)
        self.scrollWidgetLayout.addWidget(self.group_texTranslucency)

        self.scrollWidgetLayout.addWidget(common.QLine.HLine(self))

        self.scrollWidgetLayout.addWidget(self.OriginMesh)
        self.scrollWidgetLayout.addWidget(self.lodWidget)
        self.scrollWidgetLayout.addWidget(self.button_addlod)

        self.scrollWidgetLayout.addWidget(common.QLine.HLine(self))

        self.scrollWidgetLayout.addWidget(self.group_previewImage)
        self.scrollWidgetLayout.addWidget(self.ImagePreview,alignment=Qt.AlignmentFlag.AlignCenter)
        self.scrollWidgetLayout.addWidget(self.button_importAsset)
        self.scrollWidgetLayout.setContentsMargins(30,40,30,40)

        self.group_previewImage.textChanged.connect(self.setImagePreview)

        self.button_addlod.clicked.connect(self.addLod)
        self.lodWidgetLayout.setContentsMargins(0,0,0,0)
        self.combox_type.addItems([self.tra(item.value) for item in list(AssetType.__members__.values())])
        self.combox_type.combox.currentIndexChanged.connect(self.refreshWidget)


        self.widgetCategorysLayout.addWidget(self.combox_category)
        self.widgetCategorysLayout.addWidget(self.combox_subcategory)
        self.widgetCategorysLayout.setContentsMargins(0,0,0,0)

        self.combox_category.addItems([self.tra(item.value) for item in list(AssetCategory.__members__.values())])
        self.combox_subcategory.addItems([self.tra(item.value) for item in list(AssetSubccategory.__members__.values())])
       

        self.widgetSizeLayout.addWidget(self.combox_SurfaceSize)
        self.widgetSizeLayout.addWidget(self.checkbox_TilesVertically)
        self.widgetSizeLayout.addWidget(self.checkobx_TillesHorizontically)
        self.widgetSizeLayout.setContentsMargins(0,0,0,0)

        self.checkbox_TilesVertically.setFixedWidth(200)
        self.checkobx_TillesHorizontically.setFixedWidth(200)


        self.combox_SurfaceSize.addItems([self.tra(item.value) for item in list(AssetSize.__members__.values())])
        self.addLod()
        self.refreshWidget()
    def addTag(self):
        tag = self.leg_tags.lineEdit.text()
        self.leg_tags.lineEdit.clear()
        tagbutton = TagButton(text=tag,icon = FIF.DELETE,parent=self)
        tagbutton.index = len(self.tags)
        tagbutton.deletClicked.connect(self.deleteTag)
        tagbutton.setObjectName(f"TagButton_{tagbutton.index}")
        self.tags_flowLayout.addWidget(tagbutton)
        self.tags.append(tag)
    def deleteTag(self,index:int):
        tagbutton = self.findChild(TagButton,f"TagButton_{index}")
        self.tags.remove(tagbutton.text())
        self.tags_flowLayout.removeWidget(tagbutton)
        tagbutton.close()
    def setImagePreview(self,path):
        self.ImagePreview.setPixmap(scaleMap(250,250,path))
    def addLod(self):
        index = len(self.lods)
        group = DirectiorySelectGroup(self,self.tra(f"LOD {index}"),self.maxTextWidth,title="选择一个模型",filter="fbx file(*.fbx)",rootPath=self.rootPath)
        self.lodWidgetLayout.addWidget(group)
        self.lods.append(group)
    def refreshWidget(self):
        widgets = [self.combox_SurfaceSize,self.checkbox_TilesVertically,self.checkobx_TillesHorizontically,self.lodWidget,self.OriginMesh,self.button_addlod]
        for w in widgets:
            w.setHidden(False)
        currentIndex = self.combox_type.combox.currentIndex() 
        currentType = list(AssetType.__members__.values())[currentIndex]

        if currentType == AssetType.Assets3D:
            self.combox_SurfaceSize.setHidden(True)
            self.checkbox_TilesVertically.setHidden(True)
            self.checkobx_TillesHorizontically.setHidden(True)
        elif currentType == AssetType.Plant:
            self.combox_SurfaceSize.setHidden(True)
            self.checkbox_TilesVertically.setHidden(True)
            self.checkobx_TillesHorizontically.setHidden(True)
        elif currentType == AssetType.Surface:
            self.OriginMesh.setHidden(True)
            self.lodWidget.setHidden(True)
            self.button_addlod.setHidden(True)
        elif currentType == AssetType.Decal:
            self.OriginMesh.setHidden(True)
            self.lodWidget.setHidden(True)
            self.button_addlod.setHidden(True)
            pass
        else:
            pass
        pass
    def __initConnection(self):
        self.button_importAsset.clicked.connect(self.importAsset)
    def importAsset(self):
        if not ut.checkWriteAccess(Config.Get().remoteAssetLibrary):
            common.showDialog("错误","当前没有权限操作库")
            return
        name = self.leg_name.lineEdit.text()
        if name == "":
            self.showDialog("错误",f"请输入资产名称")
            return

        currentIndex = self.combox_type.combox.currentIndex() 
        type = list(AssetType.__members__.values())[currentIndex].value

        currentIndex = self.combox_category.combox.currentIndex()
        category = list(AssetCategory.__members__.values())[currentIndex].value


        currentIndex = self.combox_subcategory.combox.currentIndex()
        subCategory = list(AssetSubccategory.__members__.values())[currentIndex].value

        currentIndex = self.combox_SurfaceSize.combox.currentIndex()
        surfaceSize = list(AssetSize.__members__.values())[currentIndex].value


        if self.group_texAlbedo.checkbox.isChecked():
            albedo = os.path.normpath(self.group_texAlbedo.lineEdit.text())
        else:
            albedo = ""
        if self.group_texAO.checkbox.isChecked():
            ao = os.path.normpath(self.group_texAO.lineEdit.text())
        else:
            ao = ""
        if self.group_texbrush.checkbox.isChecked():
            brush = os.path.normpath(self.group_texbrush.lineEdit.text())
        else:
            brush = ""      
        if self.group_texBump.checkbox.isChecked():
            bump = os.path.normpath(self.group_texBump.lineEdit.text())
        else:
            bump = ""
        if self.group_texCavity.checkbox.isChecked():
            cavity = os.path.normpath(self.group_texCavity.lineEdit.text())
        else:
            cavity = ""
        if self.group_texDiffuse.checkbox.isChecked():
            diffuse = os.path.normpath(self.group_texDiffuse.lineEdit.text())
        else:
            diffuse = ""
        if self.group_texDisplacement.checkbox.isChecked():
            displacement = os.path.normpath(self.group_texDisplacement.lineEdit.text())
        else:
            displacement = ""
        if self.group_texFuzz.checkbox.isChecked():
            fuzz = os.path.normpath(self.group_texFuzz.lineEdit.text())
        else:
            fuzz = ""
        if self.group_texGloss.checkbox.isChecked():
            gloss = os.path.normpath(self.group_texGloss.lineEdit.text())
        else:
            gloss = ""
        if self.group_texMask.checkbox.isChecked():
            mask = os.path.normpath(self.group_texMask.lineEdit.text())
        else:
            mask = ""
        if self.group_texMetalness.checkbox.isChecked():
            metalness = os.path.normpath(self.group_texMetalness.lineEdit.text())
        else:
            metalness = ""
        if self.group_texNormal.checkbox.isChecked():
            normal = os.path.normpath(self.group_texNormal.lineEdit.text())
        else:
            normal = ""
        if self.group_texOpacity.checkbox.isChecked():
            opacity = os.path.normpath(self.group_texOpacity.lineEdit.text())
        else:
            opacity = ""
        if self.group_texRoughness.checkbox.isChecked():
            roughness = os.path.normpath(self.group_texRoughness.lineEdit.text())
        else:
            roughness = ""
        if self.group_texSpecular.checkbox.isChecked():
            specular = os.path.normpath(self.group_texSpecular.lineEdit.text())
        else:
            specular = ""
        if self.group_texTranslucency.checkbox.isChecked():
            translucency = os.path.normpath(self.group_texTranslucency.lineEdit.text())
        else:
            translucency = ""
        if self.OriginMesh.checkbox.isChecked():                                                                                                                                                                        
            orginMesh = os.path.normpath(self.OriginMesh.lineEdit.text())
        else:
            orginMesh = ""
        if self.group_previewImage.checkbox.isChecked():    
            previewImage = os.path.normpath(self.group_previewImage.lineEdit.text())
        else:
            previewImage = ""


        TilesVertically = self.checkbox_TilesVertically.isChecked()
        TillesHorizontically = self.checkobx_TillesHorizontically.isChecked()
        lods = []
        for lodwidget in self.lods:
            if lodwidget.checkbox.isChecked():
                lods.append(os.path.normpath(lodwidget.lineEdit.text()))

        mapData = dict(
            Albedo = albedo,
            AO = ao,
            Brush = brush,
            Bump = bump,
            Cavity = cavity,
            Diffuse = diffuse,
            Displacement = displacement,
            Fuzz = fuzz,
            Gloss = gloss,
            Mask = mask,
            Metalness = metalness,
            Normal = normal,
            Opacity = opacity,
            Roughness = roughness,
            Specular = specular,
            Translucency = translucency,
        )
        assetData = dict(
            name = name,
            tags = self.tags,
            type = type,
            surfaceSize = surfaceSize,
            TilesVertically = TilesVertically,
            TillesHorizontically = TillesHorizontically,
            category = category,
            subCategory = subCategory,
            mapData = mapData,
            orginMesh =orginMesh,
            lods = lods,
            previewImage = previewImage,
        )
        self.startImported.emit()
        makeAssetWorker = MakeAssetWorker(assetData,self)
        makeAssetWorker.onFinished.connect(self.importFinished)
        makeAssetWorker.start()
        self.setEnabled(False)
    def showDialog(self,title,content):
        w = Dialog(title,content)
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        return(w.exec())
    def importFinished(self):
        self.endImported.emit(self.index)
class TabBar(QTabBar):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
class TabWidget(QTabWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.backgroundColor = QColor(39,39,39,255)
        self.tabBar().setHidden(True)
    def paintEvent(self, a0: QPaintEvent | None) -> None:
        # painter = QPainter(self)
        # painter.fillRect(0,0,painter.device().width(),painter.device().height(),self.backgroundColor)
        # painter.end()
        pass
    def tabClose(self,index:int):
        self.removeTab(index)

class ImportInterface(QWidget,Translator):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.rootLayout = QHBoxLayout(self)
        self.ImportItemButtonWidget = QWidget(self)
        self.ImportItemButtonWidgetLayout = QVBoxLayout(self.ImportItemButtonWidget)
        self.itemButtonListWidget = QWidget(self.ImportItemButtonWidget)
        self.itemButtonListWidgetLayout = QVBoxLayout(self.itemButtonListWidget)
        self.addNewAssetWidget = QWidget(self.ImportItemButtonWidget)
        self.addNewAssetWidgetLayout = QHBoxLayout(self.addNewAssetWidget)
        self.addNewAssetLabel = QLabel(self.addNewAssetWidget,text=self.tra("ASSETS"))
        self.addNewAssetButton = PushButton(parent=self.addNewAssetWidget)
        self.switchWidget = TabWidget(self)

        self.itemButtons:list[TabBarButton]= []
        self.currentItemIndex:int = -1

        self.__initWidget()
        self.__initConnection()
        self.__setQss()
    def __initWidget(self):
        self.setObjectName("import_interface")
        self.rootLayout.addWidget(self.ImportItemButtonWidget)
        self.rootLayout.addWidget(self.switchWidget)
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.setSpacing(0)

        self.ImportItemButtonWidget.setFixedWidth(200)


        self.ImportItemButtonWidgetLayout.addWidget(self.addNewAssetWidget)
        self.ImportItemButtonWidgetLayout.addWidget(self.itemButtonListWidget)
        self.ImportItemButtonWidgetLayout.setContentsMargins(0,0,0,0)
        self.ImportItemButtonWidgetLayout.setAlignment(Qt.AlignTop)
        self.ImportItemButtonWidgetLayout.setSpacing(25)


        self.itemButtonListWidgetLayout.setSpacing(25)
        self.itemButtonListWidgetLayout.setContentsMargins(0,0,0,0)
        self.itemButtonListWidgetLayout.setAlignment(Qt.AlignTop)

        self.ImportItemButtonWidget.setObjectName("ImportItemButtonWidget")
        

        self.addNewAssetWidget.setObjectName("addNewAssetWidget")

        self.addNewAssetWidgetLayout.addWidget(self.addNewAssetLabel)
        self.addNewAssetWidgetLayout.addWidget(self.addNewAssetButton)
        self.addNewAssetWidgetLayout.setContentsMargins(15,30,10,30)

        self.addNewAssetButton.setFixedSize(23,23)


        self.prograssRing = IndeterminateProgressRing(self)
        self.prograssRing.setVisible(False)

    def __initConnection(self):
        self.addNewAssetButton.clicked.connect(self.addItem)
    def addItem(self)->None:
        # 通过对话框选取目录,如果路径为空,则跳过
        folder = QFileDialog.getExistingDirectory(self,"选择资产目录")
        if folder == "":
            return
        # 按照文件类型获取目录下的文件
        files = ClassifyFilesFormFolder(folder)

        # 获取资产名称
        assetName = files["assetName"]


        button = TabBarButton(self.ImportItemButtonWidget,assetName,len(self.itemButtons))
        button.delete_clicked.connect(self.removeItem)
        button.clicked.connect(self.setCurrentItem)
        self.itemButtons.append(button)

        importSettings = ImportSettings(self.switchWidget,self.switchWidget.count(),folder)
        importSettings.leg_name.lineEdit.textChanged.connect(button.setText)
        importSettings.leg_name.lineEdit.setText(assetName)
        importSettings.button = button
        importSettings.endImported.connect(self.endImport)
        importSettings.startImported.connect(self.startImport)

        self.itemButtonListWidgetLayout.addWidget(button)
        self.switchWidget.addTab(importSettings,assetName)
        self.setCurrentItem(button.index)
        hasOpacity = False
        for image in files["images"]:
            #使用文件名识别防止目录中出现和关键词相同的情况
            fileName = os.path.basename(image)
            for group in importSettings.textureGroups:
                if group.GroupLabel in fileName.lower():
                    group.lineEdit.setText(image)
                    group.checkbox.setChecked(True)
                    if group.GroupLabel == "opacity":
                        hasOpacity = True
            if ".jpg" in fileName.lower():
                importSettings.group_previewImage.lineEdit.setText(image)
                importSettings.group_previewImage.checkbox.setChecked(True)
        if files["models"] == []:
            if hasOpacity:
                importSettings.combox_type.combox.setCurrentText(self.tra(AssetType.Decal.value))
            else:
                importSettings.combox_type.combox.setCurrentText(self.tra(AssetType.Surface.value))
        lodIndexs = {}
        for meshUri in files["models"]:
            if ".fbx" in meshUri.lower() and "lod" not in meshUri.lower():
                importSettings.OriginMesh.lineEdit.setText(meshUri)
                importSettings.OriginMesh.checkbox.setChecked(True)
            elif "lod" in meshUri.lower():
                t = meshUri.lower().find("lod") + 3
                level = meshUri[t:t+1]
                lodIndexs[level] = meshUri
        for i in range(len(lodIndexs)-1):
            importSettings.addLod()
        for l in lodIndexs.keys():
            importSettings.lods[int(l)].lineEdit.setText(lodIndexs[l])
            importSettings.lods[int(l)].checkbox.setChecked(True)
        importSettings.refreshWidget()
    def removeItem(self,index:int):
        if not ut.checkWriteAccess(Config.Get().remoteAssetLibrary):
            common.showDialog("错误","当前没有权限操作库")
            return
        button = self.itemButtons[index]
        button.close()
        self.itemButtonListWidgetLayout.removeWidget(button)
        self.itemButtons.pop(index)

        self.switchWidget.removeTab(index)

        for i in range(len(self.itemButtons)):
            self.itemButtons[i].index = i
            self.switchWidget.widget(i).index = i
        if self.currentItemIndex == index:
            if index != 0:
                self.setCurrentItem(index-1)
            elif len(self.itemButtons) > 0:
                self.setCurrentItem(0)
            else:
                self.setCurrentItem(-1)
    def setCurrentItem(self,index:int):
        if self.currentItemIndex > -1 and self.currentItemIndex < len(self.itemButtons):
            self.itemButtons[self.currentItemIndex].setSelected(False)
        if index > -1:
            self.itemButtons[index].setSelected(True)
            self.switchWidget.setCurrentIndex(index)
        self.currentItemIndex = index
    def startImport(self):
        self.prograssRing.setVisible(True)
        self.prograssRing.move(int(self.width()/2),int(self.height()/2))
        self.setEnabled(False)
        pass
    def endImport(self,index:int):
        InfoBar.success(
            title=self.tra('notice:'),
            content=f"{self.tra('Asset')} {self.itemButtons[index].label.text()} {self.tra('is imported')}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        self.removeItem(index)
        self.prograssRing.setVisible(False)
        self.setEnabled(True)
    def __setQss(self):
        StyleSheet.IMPORT_INTERFACE.apply(self)



    