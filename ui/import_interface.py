# coding: utf-8
from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,toggleTheme,NavigationItemPosition,
                            TitleLabel,CheckBox,LineEdit,LineEditButton)
from qfluentwidgets import FluentIcon as FIF


from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QLabel,QLineEdit,QTabWidget,
                             QPushButton,QFileDialog)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)

from PyQt5.QtCore import QSize,pyqtSignal


from core.style_sheet import StyleSheet


from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve



from core.common_widget import QLine
from core.utility import AssetCategory,AssetSize,AssetSubccategory,AssetType,ClassifyFilesFormFolder,MakeAssetByData
    

class SelectFileLineEdit(LineEdit):
    selectedFile = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.openBrowserButton = LineEditButton(FIF.FOLDER, self)
        self.openBrowserButton.setIconSize(QSize(self.openBrowserButton.width()-4,self.openBrowserButton.width()-4))
        self.hBoxLayout.addWidget(self.openBrowserButton, 0, Qt.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)
        self.title = "选择一个文件"
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
    def __initWidget(self):
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.addWidget(self.checkbox)
        self.rootLayout.addWidget(self.label)
        self.rootLayout.addWidget(self.lineEdit)
        self.label.setFixedWidth(self.texMaxWidth-15)
        self.checkbox.setFixedWidth(15)
    def __initConnections(self):
        self.lineEdit.selectedFile.connect(lambda: self.checkbox.setChecked(True))
        self.checkbox.stateChanged.connect(self.selectFile)
        pass
    def selectFile(self):
        if self.checkbox.isChecked() and self.lineEdit.text() == "":
            self.lineEdit.selectFile()


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

class ImportItemButton(QWidget):
    clicked = pyqtSignal(QWidget)
    delete_clicked = pyqtSignal(QWidget)
    def __init__(self, parent,text:str):
        super().__init__(parent)
        self.rootLayout = QHBoxLayout(self)
        self.selectedFlageWidth = 5
        self.setFixedSize(200, 25)
        self.label = QLabel(self,text=text)
        self.isSelected = False
        self.button_delete = PushButton(self)

        self.__initWidget()
        self.__initConnection()
    def __initWidget(self):

        self.rootLayout.addWidget(self.label)
        self.rootLayout.addWidget(self.button_delete)
        self.rootLayout.setContentsMargins(self.selectedFlageWidth+10,0,30,0)


        self.button_delete.setFixedSize(self.height()-2,self.height()-2)
        pass
    def __initConnection(self):
        self.button_delete.clicked.connect(lambda :self.delete_clicked.emit(self))
    def paintEvent(self, a0: QPaintEvent | None) -> None:
        super().paintEvent(a0) 
        if not self.isSelected:
            return
        painter = QPainter(self)
        painter.begin(self)
        rect = QRect(0,0,self.selectedFlageWidth,self.height())
        painter.fillRect(rect,QColor(139,194,74,255))
    def setSelected(self,isSelected:bool,force=False):
        if isSelected == self.isSelected and not force:
            return
        self.isSelected = isSelected
        self.setProperty("isSelected",self.isSelected)
        self.setStyle(QApplication.style())
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if self.isSelected:
            return
        self.clicked.emit(self)
    def setText(self,text:str):
        self.label.setText(text)

class ImportSettings(QWidget):
    def __init__(self, parent,rootpath:str = "."):
        super().__init__(parent)
        #value
        self.maxTextWidth = 150
        self.texFilter = "png(*.png);;exr(*.exr);;jpeg(*.jpg)"
        self.lods:list[DirectiorySelectGroup] = []
        self.rootPath = rootpath
        #widget
        self.rootLayout = QVBoxLayout(self)

        self.scrollArea = SmoothScrollArea(self)
        self.scrollWidget = QWidget(self.scrollArea)
        self.scrollWidgetLayout = QVBoxLayout(self.scrollWidget)



        self.label_nameTga = TitleLabel(self.tr("Import Settings"),self)
        self.name = LineEidtGroup(self,self.tr("Name"),self.maxTextWidth)
        self.tags = LineEidtGroup(self,"Tags",self.maxTextWidth)
        
        self.widgetType = ComboxGroup(self,self.tr("Type"),self.maxTextWidth)

        self.widgetCategorys = QWidget(self)
        self.widgetCategorysLayout = QHBoxLayout(self.widgetCategorys)

        self.combox_category = ComboxGroup(self.widgetCategorys,self.tr("Category"),self.maxTextWidth)
        self.combox_subcategory = ComboxGroup(self.widgetCategorys,self.tr("Subcategory"),self.maxTextWidth)

        self.widgetSize = QWidget(self)
        self.widgetSizeLayout = QHBoxLayout(self.widgetSize)

        
        self.combox_SurfaceSize = ComboxGroup(self.widgetSize,self.tr("Surface Size"),self.maxTextWidth)
        self.checkbox_TilesVertically = CheckBox(self.tr("Tiles Vertically"),self.widgetSize)
        self.checkobx_TillesHorizontically = CheckBox(self.tr("Tiles Horizontically"),self.widgetSize)

        self.group_texAlbedo = DirectiorySelectGroup(self,self.tr("Albedo"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texAO = DirectiorySelectGroup(self,self.tr("AO"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texBump = DirectiorySelectGroup(self,self.tr("Bump"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texCavity= DirectiorySelectGroup(self,self.tr("Cavity"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texDiffuse = DirectiorySelectGroup(self,self.tr("Diffuse"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texDisplacement = DirectiorySelectGroup(self,self.tr("Displacement"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texFuzz = DirectiorySelectGroup(self,self.tr("Fuzz"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texGloss = DirectiorySelectGroup(self,self.tr("Gloss"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texMask = DirectiorySelectGroup(self,self.tr("Mask"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texMetalness = DirectiorySelectGroup(self,self.tr("Metalness"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texNormal = DirectiorySelectGroup(self,self.tr("Normal"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texOpacity = DirectiorySelectGroup(self,self.tr("Opacity"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texRoughness = DirectiorySelectGroup(self,self.tr("Roughness"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texSpecular = DirectiorySelectGroup(self,self.tr("Specular"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)
        self.group_texTranslucency = DirectiorySelectGroup(self,self.tr("Translucency"),self.maxTextWidth,filter=self.texFilter,rootPath=self.rootPath)

        self.OriginMesh =  DirectiorySelectGroup(self,self.tr(f"Mesh"),self.maxTextWidth,title="选择一个模型",filter="fbx file(*.fbx)",rootPath=self.rootPath)

        self.lodWidget = QWidget(self.scrollWidget)
        self.lodWidgetLayout = QVBoxLayout(self.lodWidget)
        self.button_addlod = PushButton("添加lod模型",self.scrollWidget)
        
        self.group_previewImage = DirectiorySelectGroup(self,self.tr("Preview Image"),self.maxTextWidth,filter="all files(*)",rootPath=self.rootPath)
        self.button_importAsset = PushButton("Import",self)
        
        self.__initWidget()
        self.__initConnection()
    def __initWidget(self):
        self.rootLayout.setContentsMargins(0,0,0,0)
        
        self.rootLayout.addWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("ImportSettingsScrollArea")


        self.scrollWidget.setObjectName("ScrollWidget")




        self.scrollWidgetLayout.addWidget(self.label_nameTga)
        self.scrollWidgetLayout.addWidget(self.name)
        self.scrollWidgetLayout.addWidget(self.tags)
        self.scrollWidgetLayout.addWidget(QLine.HLine(self))
        self.scrollWidgetLayout.addWidget(self.widgetType)
        self.scrollWidgetLayout.addWidget(self.widgetCategorys)
        self.scrollWidgetLayout.addWidget(self.widgetSize)
        self.scrollWidgetLayout.addWidget(QLine.HLine(self))
        self.scrollWidgetLayout.addWidget(self.group_texAlbedo)
        self.scrollWidgetLayout.addWidget(self.group_texAO)
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
        self.scrollWidgetLayout.addWidget(QLine.HLine(self))
        self.scrollWidgetLayout.setContentsMargins(30,40,30,40)

        self.scrollWidgetLayout.addWidget(self.OriginMesh)
        self.scrollWidgetLayout.addWidget(self.lodWidget)
        self.scrollWidgetLayout.addWidget(self.button_addlod)
        self.scrollWidgetLayout.addWidget(QLine.HLine(self))
        self.scrollWidgetLayout.addWidget(self.group_previewImage)
        self.scrollWidgetLayout.addWidget(self.button_importAsset)



        self.button_addlod.clicked.connect(self.addLod)

        self.lodWidgetLayout.setContentsMargins(0,0,0,0)

        self.widgetType.addItems([self.tr(item.value) for item in list(AssetType.__members__.values())])
        self.widgetType.combox.currentIndexChanged.connect(self.refreshWidget)


        self.widgetCategorysLayout.addWidget(self.combox_category)
        self.widgetCategorysLayout.addWidget(self.combox_subcategory)
        self.widgetCategorysLayout.setContentsMargins(0,0,0,0)

        self.combox_category.addItems([self.tr(item.value) for item in list(AssetCategory.__members__.values())])
        self.combox_subcategory.addItems([self.tr(item.value) for item in list(AssetSubccategory.__members__.values())])
       

        self.widgetSizeLayout.addWidget(self.combox_SurfaceSize)
        self.widgetSizeLayout.addWidget(self.checkbox_TilesVertically)
        self.widgetSizeLayout.addWidget(self.checkobx_TillesHorizontically)
        self.widgetSizeLayout.setContentsMargins(0,0,0,0)

        self.checkbox_TilesVertically.setFixedWidth(200)
        self.checkobx_TillesHorizontically.setFixedWidth(200)


        self.combox_SurfaceSize.addItems([self.tr(item.value) for item in list(AssetSize.__members__.values())])
        self.addLod()
        self.refreshWidget()
    def addLod(self):
        index = len(self.lods)
        group = DirectiorySelectGroup(self,self.tr(f"LOD {index}"),self.maxTextWidth,title="选择一个模型",filter="fbx file(*.fbx)",rootPath=self.rootPath)
        self.lodWidgetLayout.addWidget(group)
        self.lods.append(group)
    def refreshWidget(self):
        widgets = [self.combox_SurfaceSize,self.checkbox_TilesVertically,self.checkobx_TillesHorizontically,self.lodWidget,self.OriginMesh,self.button_addlod]
        for w in widgets:
            w.setHidden(False)
        if self.widgetType.combox.currentText() == AssetType.Assets3D.value:
            self.combox_SurfaceSize.setHidden(True)
            self.checkbox_TilesVertically.setHidden(True)
            self.checkobx_TillesHorizontically.setHidden(True)
        elif self.widgetType.combox.currentText() == AssetType.Surface.value:
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
        name = self.name.lineEdit.text()
        tags = self.tags.lineEdit.text()
        type = AssetType._value2member_map_[self.widgetType.combox.currentText()]
        albedo = self.group_texAlbedo.lineEdit.text()
        ao = self.group_texAO.lineEdit.text()
        bump = self.group_texBump.lineEdit.text()
        cavity = self.group_texCavity.lineEdit.text()
        diffuse = self.group_texDiffuse.lineEdit.text()
        displacement = self.group_texDisplacement.lineEdit.text()
        fuzz = self.group_texFuzz.lineEdit.text()
        gloss = self.group_texGloss.lineEdit.text()
        mask = self.group_texMask.lineEdit.text()
        metalness = self.group_texMetalness.lineEdit.text()
        normal = self.group_texNormal.lineEdit.text()
        opacity = self.group_texOpacity.lineEdit.text()
        roughness = self.group_texRoughness.lineEdit.text()
        specular = self.group_texSpecular.lineEdit.text()
        translucency = self.group_texTranslucency.lineEdit.text()
        orginMesh = self.OriginMesh.lineEdit.text()
        lods = []
        for lodwidget in self.lods:
            lods.append(lodwidget.lineEdit.text())
        previewImage = self.group_previewImage.lineEdit.text()

        assetData = dict(
            name = name,
            tags = tags,
            type = type,
            albedo = albedo,
            ao = ao,
            bump = bump,
            cavity = cavity,
            diffuse = diffuse,
            displacement = displacement,
            fuzz = fuzz,
            gloss = gloss,
            mask = mask,
            metalness = metalness,
            normal = normal,
            opacity = opacity,
            roughness = roughness,
            specular = specular,
            translucency = translucency,
            orginMesh =orginMesh,
            lods = lods,
            previewImage = previewImage
        )
        asset = MakeAssetByData(assetData)
        



class ImportInterface(QWidget):
    def __init__(self, parent):
        super().__init__(parent)


        self.rootLayout = QHBoxLayout(self)
        self.ImportItemButtonWidget = QWidget(self)
        self.ImportItemButtonWidgetLayout = QVBoxLayout(self.ImportItemButtonWidget)
        self.itemButtonListWidget = QWidget(self.ImportItemButtonWidget)
        self.itemButtonListWidgetLayout = QVBoxLayout(self.itemButtonListWidget)
        self.addNewAssetWidget = QWidget(self.ImportItemButtonWidget)
        self.addNewAssetWidgetLayout = QHBoxLayout(self.addNewAssetWidget)
        self.addNewAssetLabel = QLabel(self.addNewAssetWidget,text=self.tr("ASSETS"))
        self.addNewAssetButton = PushButton(parent=self.addNewAssetWidget)
        self.switchWidget = QTabWidget(self)

        self.items:dict= {}

        self.currentButton:ImportItemButton = None

        self.__initWidget()
        self.__initConnection()
        self.__setQss()
        self.setObjectName("import_interface")
    def __initWidget(self):
        self.rootLayout.addWidget(self.ImportItemButtonWidget)
        self.rootLayout.addWidget(self.switchWidget)
        self.rootLayout.setContentsMargins(0,0,0,0)

        self.ImportItemButtonWidget.setFixedWidth(200)
        self.switchWidget.setAutoFillBackground(True)
        self.switchWidget.tabBar().setHidden(True)
        self.switchWidget.setObjectName("ImportInterfaceSwicthWidget")


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

    def __initConnection(self):
        self.addNewAssetButton.clicked.connect(self.addNewAsset)
    def addNewAsset(self):
        folder = QFileDialog.getExistingDirectory(self,"选择资产目录")
        files = ClassifyFilesFormFolder(folder)
        imsettings = self.addItem(files["assetName"],folder)
        
    def addItem(self,assetName:str,rootPath:str=".")->ImportSettings:
        button = ImportItemButton(self.ImportItemButtonWidget,assetName)
        button.delete_clicked.connect(self.removeItem)
        button.clicked.connect(self.setCurrentItem)
        importSettings = ImportSettings(self.switchWidget,rootPath)
        importSettings.name.lineEdit.textChanged.connect(button.setText)
        importSettings.name.lineEdit.setText(assetName)
        self.items[button] = importSettings
        self.itemButtonListWidgetLayout.addWidget(button)
        self.switchWidget.addTab(importSettings,assetName)
        self.setCurrentItem(button)
        return importSettings
    def removeItem(self,button):
        importSettings = self.items[button]
        for i in range(self.switchWidget.count()):
            if self.switchWidget.currentWidget() == importSettings:
                self.switchWidget.removeTab(i)
        self.itemButtonListWidgetLayout.removeWidget(button)
        self.items.pop(button)
        if button == self.currentButton:
            if len(self.items) != 0:
                self.setCurrentItem(list(self.items.keys())[0])
            else:
                self.setCurrentItem(None)
    def setCurrentItem(self,button:ImportItemButton):
        if self.currentButton:
            self.currentButton.setSelected(False)
        if button:
            button.setSelected(True)
            importSettings = self.items[button]
            for i in range(self.switchWidget.count()):
                if self.switchWidget.currentWidget() == importSettings:
                    self.switchWidget.setCurrentIndex(i)
        self.currentButton = button
    def __setQss(self):
        StyleSheet.IMPORT_INTERFACE.apply(self)

