
# coding: utf-8
from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,toggleTheme,NavigationItemPosition,
                            TitleLabel,CheckBox,LineEdit,LineEditButton)
from qfluentwidgets import FluentIcon as FIF


from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QLabel,QLineEdit,QTabWidget,
                             QPushButton)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)

from PyQt5.QtCore import QSize,pyqtSignal


from core.style_sheet import StyleSheet



from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve


import sys

from core.Log import log

from ui.home_interface import HomeInterface
from ui.setting_interface import SettingInterface
from enum import Enum



class AssetType(Enum):
    Assets3D = "3D Assets"
    Surface = "Surface"

class AssetCategory(Enum):
    Building   = "Building"
    Food       = "Food"
    Historical = "Historical"
    Industrial = "Industrial"

class AssetSubccategory(Enum):
    Floating = "Floating"
    Shore    = "Shore"
    Submerged = "Submerged"




class QLine(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFrameShadow(QFrame.Shadow.Sunken)
    def SetHorizontal(self):
        self.setFrameShape(QFrame.Shape.HLine)
    def SetVertical(self):
        self.setFrameShape(QFrame.Shape.VLine)
    @classmethod
    def HLine(cls,parent):
        line = QLine(parent)
        line.SetHorizontal()
        return line
    @classmethod
    def VLine(cls,parent):
        line = QLine(parent)
        line.SetVertical()
        return line
    

class SelectFileLineEdit(LineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.openBrowserButton = LineEditButton(FIF.FOLDER, self)

        self.hBoxLayout.addWidget(self.openBrowserButton, 0, Qt.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        
class DirectiorySelectGroup(QWidget):
    def __init__(self, parent,text:str):
        super().__init__(parent)
        self.rootLayout = QHBoxLayout(self)

        self.checkbox = CheckBox(self.tr(text),self)
        self.lineEdit = SelectFileLineEdit(self)

        self.__initWidget()
    def __initWidget(self):
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.addWidget(self.checkbox)
        self.rootLayout.addWidget(self.lineEdit)


class LineEidtGroup(QWidget):
    def __init__(self, parent,text:str,textMaxWidth:int = 50):
        super().__init__(parent)
        self.textMaxWidth = textMaxWidth

        self.rootLayout = QHBoxLayout(self)
        self.labelText =QLabel(self,text=text)
        self.lineEdit = QLineEdit(self)
        self.__initWidget()
    def __initWidget(self):
        self.rootLayout.addWidget(self.labelText)
        self.rootLayout.addWidget(self.lineEdit)
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.labelText.setMinimumWidth(self.textMaxWidth)

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
        self.labelText.setMinimumWidth(self.textMaxWidth)
    def addItems(self,items:list[str]):
        self.combox.addItems(items)


class ImportItemButton(QWidget):
    def __init__(self, parent,text:str,index:int):
        super().__init__(parent)
        self.index = index
        self.rootLayout = QHBoxLayout(self)
        self.selectedFlageWidth = 5
        self.setFixedSize(200, 25)
        self.label = QLabel(self,text=text)

        self.button_delete = PushButton(self)


        self.__initWidget()
    def __initWidget(self):

        self.rootLayout.addWidget(self.label)
        self.rootLayout.addWidget(self.button_delete)
        self.rootLayout.setContentsMargins(self.selectedFlageWidth+10,0,30,0)


        self.button_delete.setFixedSize(self.height()-2,self.height()-2)
        pass
    def paintEvent(self, a0: QPaintEvent | None) -> None:
        super().paintEvent(a0) 



        painter = QPainter(self)
        painter.begin(self)
        rect = QRect(0,0,self.selectedFlageWidth,self.height())
        painter.fillRect(rect,QColor(139,194,74,255))

        painter.end()


class InportSettings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        #value
        self.type = AssetType.Assets3D
        self.maxTextWidth = 150
        #widget
        self.rootLayout = QVBoxLayout(self)



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

        self.group_texAlbedo = DirectiorySelectGroup(self,self.tr("Albedo"))
        self.group_texAO = DirectiorySelectGroup(self,self.tr("AO"))
        self.group_texBump = DirectiorySelectGroup(self,self.tr("Bump"))
        self.group_texCavity= DirectiorySelectGroup(self,self.tr("Cavity"))
        self.group_texDiffuse = DirectiorySelectGroup(self,self.tr("Diffuse"))
        self.group_texDisplacement = DirectiorySelectGroup(self,self.tr("Displacement"))
        self.group_texFuzz = DirectiorySelectGroup(self,self.tr("Fuzz"))
        self.group_texGloss = DirectiorySelectGroup(self,self.tr("Gloss"))
        self.group_texMask = DirectiorySelectGroup(self,self.tr("Mask"))
        self.group_texMetalness = DirectiorySelectGroup(self,self.tr("Metalness"))
        self.group_texNormal = DirectiorySelectGroup(self,self.tr("Normal"))
        self.group_texOpacity = DirectiorySelectGroup(self,self.tr("Opacity"))
        self.group_texRoughness = DirectiorySelectGroup(self,self.tr("Roughness"))
        self.group_texSpecular = DirectiorySelectGroup(self,self.tr("Specular"))
        self.group_texTranslucency = DirectiorySelectGroup(self,self.tr("Translucency"))
        self.__initWidget()
    def __initWidget(self):
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.addWidget(self.label_nameTga)
        self.rootLayout.addWidget(self.name)
        self.rootLayout.addWidget(self.tags)
        self.rootLayout.addWidget(QLine.HLine(self))
        self.rootLayout.addWidget(self.widgetCategorys)
        self.rootLayout.addWidget(self.widgetSize)
        self.rootLayout.addWidget(self.widgetType)
        self.rootLayout.addWidget(QLine.HLine(self))
        self.rootLayout.addWidget(self.group_texAlbedo)
        self.rootLayout.addWidget(self.group_texAO)
        self.rootLayout.addWidget(self.group_texBump)
        self.rootLayout.addWidget(self.group_texCavity)
        self.rootLayout.addWidget(self.group_texDiffuse)
        self.rootLayout.addWidget(self.group_texDisplacement)
        self.rootLayout.addWidget(self.group_texFuzz)
        self.rootLayout.addWidget(self.group_texGloss)
        self.rootLayout.addWidget(self.group_texMask)
        self.rootLayout.addWidget(self.group_texMetalness)
        self.rootLayout.addWidget(self.group_texNormal)
        self.rootLayout.addWidget(self.group_texOpacity)
        self.rootLayout.addWidget(self.group_texRoughness)
        self.rootLayout.addWidget(self.group_texSpecular)
        self.rootLayout.addWidget(self.group_texTranslucency)
        self.rootLayout.addWidget(QLine.HLine(self))

        self.widgetType.addItems([self.tr(item) for item in AssetType._member_names_])

        self.widgetCategorysLayout.addWidget(self.combox_category)
        self.widgetCategorysLayout.addWidget(self.combox_subcategory)

        self.combox_category.addItems([self.tr(item) for item in AssetCategory._member_names_])
        self.combox_subcategory.addItems([self.tr(item) for item in AssetSubccategory._member_names_])


        self.widgetSizeLayout.addWidget(self.combox_SurfaceSize)
        self.widgetSizeLayout.addWidget(self.checkbox_TilesVertically)
        self.widgetSizeLayout.addWidget(self.checkobx_TillesHorizontically)

        surfaceSize = [1,2,3,4]
        self.combox_SurfaceSize.addItems([str(item) + self.tr("meter") for item in surfaceSize])


        
class ImportInterface(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.tabs:list[ImportItemButton] = []

        self.rootLayout = QHBoxLayout(self)


        
        self.ImportItemButtonWidget = QWidget(self)
        self.ImportItemButtonWidgetLayout = QVBoxLayout(self.ImportItemButtonWidget)

        self.ImportItemButtonTitleLabel = QLabel(self.ImportItemButtonWidget,text=self.tr("ASSETS"))

        self.switchWidget = QTabWidget(self)



        self.__initWidget()
        self.__setQss()
        self.setObjectName("import_interface")
    def __initWidget(self):
        self.rootLayout.addWidget(self.ImportItemButtonWidget)
        self.rootLayout.addWidget(self.switchWidget)
        self.rootLayout.setContentsMargins(0,0,0,0)


        self.switchWidget.setTabBarAutoHide(True)

        self.switchWidget.setObjectName("ImportInterfaceSwicthWidget")



        self.ImportItemButtonWidgetLayout.addWidget(self.ImportItemButtonTitleLabel,alignment=Qt.AlignTop)
        self.ImportItemButtonWidgetLayout.setContentsMargins(0,0,0,0)
        self.ImportItemButtonWidgetLayout.setAlignment(Qt.AlignTop)
        self.ImportItemButtonWidget.setObjectName("ImportItemButtonWidget")

        self.ImportItemButtonTitleLabel.setFixedHeight(40)
        self.ImportItemButtonTitleLabel.setObjectName("ImportItemButtonTitleLabel")

        self.addItem("Test")

    def addItem(self,AssetName:str):
        index = self.switchWidget.addTab(InportSettings(self),AssetName)
        button = ImportItemButton(self.ImportItemButtonWidget,AssetName,index)
        self.ImportItemButtonWidgetLayout.addWidget(button,alignment=Qt.AlignTop)
        self.tabs.append(button)
    def removeItem(self,index:int):
        button = self.tabs[index]
        self.switchWidget.removeTab(button.index)
        self.ImportItemButtonWidgetLayout.removeWidget(button)
    def __setQss(self):
        StyleSheet.IMPORT_INTERFACE.apply(self)
        StyleSheet.IMPORT_INTERFACE.apply(self.switchWidget)



class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.homeInterface = HomeInterface(self)
        self.SettingInterface = SettingInterface(self)
        self.importInterface = ImportInterface(self)
        self.setMinimumSize(1200,400)

        self.__initWindow()
        self.__addSubInterface()
        self.__initNavigationInterface()
    def __addSubInterface(self):
        self.addSubInterface(self.homeInterface,FIF.HOME,"HOME")
        self.addSubInterface(self.importInterface,FIF.DOWNLOAD,"Import")
        self.addSubInterface(self.SettingInterface,FIF.SETTING,"SETTING",NavigationItemPosition.BOTTOM)
        pass
    def __initNavigationInterface(self):
        pass
    def __initWindow(self):
        self.resize(1200,800)
        self.setWindowTitle("MyBridge")

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    toggleTheme()
    window = MainWindow()
    window.show()
    app.exec()


