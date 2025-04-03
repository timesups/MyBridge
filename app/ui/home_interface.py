from qfluentwidgets import (FlowLayout,PushButton,
                            SmoothScrollArea,SearchLineEdit,
                            ComboBox,InfoBar,InfoBarPosition,Dialog)
from PyQt5.QtWidgets import (QApplication,QWidget,
                             QFrame,QHBoxLayout,QVBoxLayout,QMenu,
                             QLabel,QSizePolicy)
from PyQt5.QtGui import (QCloseEvent, QContextMenuEvent, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QPixmap,QColor, 
                         QResizeEvent,QTransform)
from PyQt5.QtCore import QEvent, QRect,Qt,pyqtSignal,QThread
import pyperclip

import os

from app.core.Log import Log
from app.core.style_sheet import StyleSheet
from app.core.common_widgets import scalePixelMap,scaleMap,StringButton,LoadPixmapSafely
import app.core.utility as ut
from app.core.config import Config

from app.core.translator import Translator
from app.core.icons import Icons

from ..core.backend import Backend
from .assets_import_interface import AssetsEditInterface

class ItemCardContextMenu(QMenu):
    def __init__(self,parent=None):
        super().__init__(parent)

class ImageScaleWorker(QThread):
    width = 100
    height = 100
    imageOrigin = None
    image = None
    def run(self):
        self.image = scalePixelMap(self.width,self.height,self.imageOrigin)

class ItemCard(QFrame):
    clicked = pyqtSignal(int)
    goToFile = pyqtSignal(int)
    deleteItem = pyqtSignal(int)
    editItem = pyqtSignal(int)
    def __init__(self,parent,index:int,imagePath:str,name:str,assetid:str,size:int=250):
        super().__init__(parent=parent)
        self.setFixedSize(size,size)
        self.item_pixel_map = LoadPixmapSafely(imagePath)
        self.item_name = name
        self.__textPaddingX = 5
        self.__textPaddingY = 5
        self.isSelected = False
        self.index = index
        self.isHove = False
        self.imageMargin = 8
        self.worker = ImageScaleWorker(self)
        self.isFavorite = False
        self.heartPixmap = Icons.get().heart
        self.assetid = assetid
        self.action_edit = None
    def setSize(self,size:int):
        self.resize(size,size)
        self.setFixedSize(size,size)
    def setSelected(self,isSelected:bool,force=False):
        if isSelected == self.isSelected and not force:
            return
        self.isSelected = isSelected
        self.setProperty("isSelected",self.isSelected)
        self.setStyle(QApplication.style())
    def contextMenuEvent(self, a0: QContextMenuEvent | None) -> None:
        menu = ItemCardContextMenu(self)
        action = menu.addAction("复制资产ID")
        action.triggered.connect(lambda :pyperclip.copy(self.assetid))

        action = menu.addAction("打开文件夹")
        action.triggered.connect(lambda :self.goToFile.emit(self.index))

        action = menu.addAction("删除资产")
        action.triggered.connect(lambda :self.deleteItem.emit(self.index))


        action = menu.addAction("编辑资产")
        action.triggered.connect(lambda :self.editItem.emit(self.index))
        

        menu.move(a0.globalPos())
        menu.show()
        pass
    def enterEvent(self, a0: QEvent | None) -> None:
        self.isHove = True
        return super().enterEvent(a0)
    def leaveEvent(self, a0: QEvent | None) -> None:
        self.isHove = False
        return super().leaveEvent(a0)
    def mouseReleaseEvent(self, e: QMouseEvent | None) -> None:
        if e.button() == 1:
            if self.isSelected:
                return
            self.clicked.emit(self.index)
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        if not self.worker.isRunning():
            self.worker.imageOrigin =  self.item_pixel_map
            self.worker.width = self.width()-2*self.imageMargin
            self.worker.height = self.height()-2*self.imageMargin
            self.worker.start()
        return super().resizeEvent(a0)
    def paintEvent(self, e: QPaintEvent | None) -> None:
        painter = QPainter(self)
        rect_tar  = QRect(self.imageMargin,self.imageMargin,self.width()-2*self.imageMargin,self.height()-2*self.imageMargin)
        if not self.worker.isRunning() and self.worker.image != None:
            rect_src  =  QRect(0,0, self.worker.image.width(),self.worker.image.height())
            painter.drawPixmap(rect_tar,self.worker.image,rect_src)
        else:
            painter.fillRect(rect_tar,QColor(34,34,34)) 
        if self.isHove and self.isEnabled():
            painter.drawText(0+self.__textPaddingX,self.height()-self.__textPaddingY,f"{self.item_name}")
        painter.end()


class InfoPanelImagePreivew(QFrame):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.backGroundImageUri = ""
        self.backGroundImage = None
        self.backGroundColor = QColor(15,15,15,255)
        self.setFixedHeight(300)
    def __reloadImage(self):
        self.backGroundImage = scaleMap(self.width(),self.height(),self.backGroundImageUri)
    def setImgae(self,imagePath:str):
        self.backGroundImageUri = imagePath
        self.__reloadImage()
    def paintEvent(self, e: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.fillRect(0,0,self.width(),self.height(),self.backGroundColor)
        brush = QBrush()
        brush.setTexture(self.backGroundImage)
        rect  = QRect(0,0,painter.device().width(),painter.device().height())
        painter.fillRect(rect,brush)
        painter.end()
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.__reloadImage()
        return super().resizeEvent(a0)


class InfoPanel(QFrame,Translator):
    onExportClicked = pyqtSignal()
    onTagClicked = pyqtSignal(str)
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.setFixedWidth(400)
        self.shadowWidth = 20
        self.maxAssetTitleLength = 15

        self.rootLayout = QVBoxLayout(self)

        self.scrollArea = SmoothScrollArea(self)
        self.scrollWidget = QWidget(self.scrollArea)
        self.scrollWidgetLayout = QVBoxLayout(self.scrollWidget)

        self.titleImage = InfoPanelImagePreivew(self)

        self.titelWidget = QWidget(self)
        self.titelWidgetLayout = QVBoxLayout(self.titelWidget)

        self.titleLabel = QLabel(self.titelWidget,text="titleLabel")
        self.typeLabel = QLabel(self.titelWidget,text="typeLabel")


        self.CategoryLabel = QLabel(self.titelWidget,text="CategoryLabel")


        self.tagsWidget = QWidget(self.titelWidget)
        self.tagsFlowLayout = FlowLayout(self.tagsWidget,False)
        self.tagsFlowLayout .setContentsMargins(10,10,10,10)
        self.tagsFlowLayout .setVerticalSpacing(20)
        self.tagsFlowLayout .setHorizontalSpacing(10)

        self.exportWidget = QWidget(self)
        self.exportWidgetLayout = QHBoxLayout(self.exportWidget)

        self.button_export = PushButton(self.tra("Export"),self.exportWidget)

        self.combox_res = ComboBox(parent=self.exportWidget)
        self.combox_res.addItems([item.value for item in list(ut.TextureSize.__members__.values())])
        self.combox_res.currentIndexChanged.connect(self.__saveConfig)


        self.combox_lod = ComboBox(parent=self.exportWidget)

        self.combox_lod.currentIndexChanged.connect(self.__saveConfig)

        self.__initWidget()
        self.__loadConfig()
    def __initWidget(self):
        self.rootLayout.addWidget(self.scrollArea)
        self.rootLayout.addWidget(self.exportWidget)
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0,0,0,0)

        self.scrollWidgetLayout.addWidget(self.titleImage)
        self.scrollWidgetLayout.addWidget(self.titelWidget)


        self.scrollWidgetLayout.setContentsMargins(0,0,0,0)
        self.scrollWidgetLayout.setSpacing(0)
        self.scrollWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollWidgetLayout.addWidget(self.tagsWidget)
        self.exportWidgetLayout.addWidget(self.combox_res)
        self.exportWidgetLayout.addWidget(self.combox_lod)
        self.exportWidgetLayout.addWidget(self.button_export)
        self.exportWidgetLayout.setContentsMargins(0,10,0,10)

        self.titelWidget.setObjectName("InfoPanelTitleWidget")
        self.titelWidgetLayout.addWidget(self.titleLabel)
        self.titelWidgetLayout.addWidget(self.typeLabel)
        self.titelWidgetLayout.addWidget(self.CategoryLabel)

        self.button_export.clicked.connect(lambda:self.onExportClicked.emit())

        self.titleLabel.setObjectName("titleLabel")
        self.typeLabel.setObjectName("typeLabel")
        self.CategoryLabel.setObjectName("typeLabel")


        self.tagsWidget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.tagsWidget.setObjectName("TagWidget")

    def setPanelInfo(self,imagePath:str,name:str,type:str,tags:list[str],category,subcategory,lods:list[int]=[]):
        self.titleImage.setImgae(imagePath)

        #裁切名称长度
        if len(name) > self.maxAssetTitleLength:
            name = name[0:self.maxAssetTitleLength] + "..."
        self.titleLabel.setText(name)
        self.typeLabel.setText(type)

        self.CategoryLabel.setText(f"{category}|{subcategory}")

        for i in range(self.tagsFlowLayout.count()):
            button = self.tagsFlowLayout.itemAt(i).widget()
            #释放内存
            button.deleteLater()
            button = None

        self.tagsFlowLayout.removeAllWidgets()
        for tag in tags:
            button = StringButton(tag)
            button.onClicked.connect(self.tagClicked)
            self.tagsFlowLayout.addWidget(button)

        self.combox_lod.clear()
        self.combox_lod.addItem(f"original")
        for lod in lods:
            self.combox_lod.addItem(f"Lod{lod}")
    def tagClicked(self,text):
        self.onTagClicked.emit(text)
    def __loadConfig(self):
        self.combox_res.setCurrentIndex(Config.Get().exportTextureSizeIndex)
        try:
            self.combox_lod.setCurrentIndex(Config.Get().exportLodIndex)
        except:
            pass
    def __saveConfig(self,index):
        Config.Get().exportTextureSizeIndex = self.combox_res.currentIndex()
        Config.Get().exportLodIndex = self.combox_lod.currentIndex()
        Config.Get().saveConfig()
        
class ItemHeader(QFrame,Translator):
    searchSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.rootLayout = QVBoxLayout(self)
        
        self.headerWidget = QWidget(self)
        self.headerWidgetLayout = QVBoxLayout(self.headerWidget)

        self.searchBar = SearchLineEdit(self.headerWidget)


        self.comboxWidget = QWidget(self.headerWidget)
        self.comboxWidgetLayout = QHBoxLayout(self.comboxWidget)


        self.combox_type = ComboBox(self)
        self.combox_type.addItem("请选择资产类型")
        self.combox_type.addItems([self.tra(item.value) for item in list(ut.AssetType.__members__.values())])
        self.combox_type.setFixedWidth(200)


        self.combox_category = ComboBox(self)
        self.combox_category.addItem("请选择资产主分类")
        self.combox_category.addItems(ut.GetCategorys(0))
        self.combox_category.setFixedWidth(200)



        self.combox_subcategory = ComboBox(self)
        self.combox_subcategory.addItem("请选择资产次级分类")
        self.combox_subcategory.setFixedWidth(200)


        self.__initWidget()

    def __initWidget(self):
        self.rootLayout.addWidget(self.headerWidget)
        self.rootLayout.setContentsMargins(15,15,15,15)
        self.headerWidgetLayout.addWidget(self.searchBar)
        self.headerWidgetLayout.addWidget(self.comboxWidget)
        self.headerWidgetLayout.setContentsMargins(0,0,0,0)

        self.comboxWidgetLayout.setContentsMargins(0,0,0,0)
        self.comboxWidgetLayout.addWidget(self.combox_type)
        self.comboxWidgetLayout.addWidget(self.combox_category)
        self.comboxWidgetLayout.addWidget(self.combox_subcategory)
        self.comboxWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchBar.searchSignal.connect(self.__search)
        self.searchBar.clearSignal.connect(self.__clear)
        self.searchBar.returnPressed.connect(lambda:self.__search(self.searchBar.text()))
    def __search(self,text:str):
        """ emit search signal """
        text = text.strip()
        if text:
            self.searchSignal.emit(text)
        else:
            self.clearSignal.emit()
    def __clear(self):
        self.clearSignal.emit()


class FlowWidget(QWidget):
    RightMouseclicked = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent=parent)
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == 1:
            self.RightMouseclicked.emit()


class MySmoothScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
    def SetValueToCurrentSelected(self,index:int):
        
        pass

class ItemCardView(QWidget,Translator):
    assetDelete = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        # values
        self.perItemSpacing = 8
        self.initPerItemCardSize = 256
        self.cards:list[ItemCard] = []
        self.flowLayoutSideMargins = 30
        self.currentSelectedIndex = -1

        # widgets
        self.rootLayout = QVBoxLayout(self)
        self.view = QFrame(self)
        self.viewLayout = QHBoxLayout(self.view)


        self.scrollArea = MySmoothScrollArea(self.view)
        self.infoPanel = InfoPanel(self)
        self.flowWidget = FlowWidget(self.scrollArea)
        self.flowLayout = FlowLayout(self.flowWidget,False,True)
        self.LoadCardCountPerTimes = 36
        self.currentLoadedCardCount = 0
        # methods
        self.__initWidget()


        self.loadItems()
    def __initWidget(self):

        self.view.setObjectName("ItemView")
        self.rootLayout.addWidget(self.view)
        self.rootLayout.setContentsMargins(0,0,0,0)



        self.viewLayout.addWidget(self.scrollArea)
        self.viewLayout.addWidget(self.infoPanel)
        self.viewLayout.setContentsMargins(0,0,0,0)

        self.scrollArea.setWidget(self.flowWidget)
        self.scrollArea.setWidgetResizable(True)#需要使组件可以重设大小
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.backgroundRole()
        self.scrollArea.setViewportMargins(0,0,0,0)
        self.scrollArea.setObjectName("ItemCardViewScrollArea")
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.loadItemsByScrollBar)


        self.flowWidget.setObjectName("flowwidget")
        self.flowWidget.RightMouseclicked.connect(lambda: self.setSelectedItem(-1))

        self.infoPanel.onExportClicked.connect(self.exportToUnreal)


        self.flowLayout.setVerticalSpacing(self.perItemSpacing)
        self.flowLayout.setHorizontalSpacing(self.perItemSpacing)
        self.flowLayout.setContentsMargins(self.flowLayoutSideMargins,0,self.flowLayoutSideMargins,0)
        # 默认关闭信息面板
        self.infoPanel.close()

        # 从数据库加载数据
        self.filteredAssetDatas = self.loadItemFromDataBaseAndMakeItAbs()
    def loadItemsByScrollBar(self,value):
        if value/(self.scrollArea.verticalScrollBar().maximum()+0.1) >= 0.98:
            self.loadItems()
    def setPerCardSize(self,size):
        for card in self.cards:
            card.setSize(size)
    def setSelectedItem(self,index:int):
        Log(f"设置当前选中的索引为{index}","HomePage")
        #清除当前选择的项目
        if len(self.cards) > 0 and self.currentSelectedIndex < len(self.cards):
            self.cards[self.currentSelectedIndex].setSelected(False)
        self.infoPanel.close()
        #如果输入的索引大于0,表示选中了有效的项目,否则说明只是清空项目
        if index >=0:
            libraryAssetData = self.filteredAssetDatas[index]
            self.cards[index].setSelected(True)
            self.infoPanel.setPanelInfo(
                libraryAssetData["previewFile"],
                libraryAssetData["name"],
                self.tra(libraryAssetData["type"]),
                libraryAssetData["tags"],
                libraryAssetData["category"],
                libraryAssetData["subcategory"],
                libraryAssetData["lods"]
                )
            self.infoPanel.show()
            self.scrollArea.SetValueToCurrentSelected(self.currentSelectedIndex)
        self.currentSelectedIndex = index
    def clearAllCards(self):
        self.flowLayout.removeAllWidgets()
        for card in self.cards:
            card.close()
            card.deleteLater()
            card = None
        self.cards = []
    def loadItems(self):
        for i in range(self.currentLoadedCardCount,self.currentLoadedCardCount+self.LoadCardCountPerTimes):
            if i < len(self.filteredAssetDatas):
                self.addItemCard(self.filteredAssetDatas[i]["previewFile"],self.filteredAssetDatas[i]["name"],self.filteredAssetDatas[i]["AssetID"])
                self.currentLoadedCardCount+=1
            else:
                return
    def loadItemFromDataBaseAndMakeItAbs(self):
        if Backend.Get().isBackendAvailable():
            datas = Backend.Get().getAssetsList()
            remoteAssetLibrary = Backend.Get().getAssetRootPath()
        else:
            datas = []
        newDatas = []
        for data in datas:
            data["rootFolder"] = os.path.join(remoteAssetLibrary,data["rootFolder"])
            data["previewFile"] = os.path.join(remoteAssetLibrary,data["rootFolder"],data["previewFile"])
            data["jsonUri"] =os.path.join(remoteAssetLibrary,data["rootFolder"],data["jsonUri"])
            newDatas.append(data)
        self.loadedAsset = newDatas
        return newDatas
    def FilterCards(self,type_index:int,category_index:int,subcategory_index:int,search_key_word:str):
        #load all assets
        self.clearAllCards()
        self.filteredAssetDatas = []
        for assetData in self.loadedAsset:
            if type_index >= 1:
                type = list(ut.AssetType.__members__.values())[type_index-1]
                if type.value != assetData['type']:
                    continue
            if category_index >= 1:
                category = ut.GetCategorys(0)[category_index-1]
                if category != assetData['category']:
                    continue
            if subcategory_index >=1:
                subcategory = ut.GetSubCategorys(category_index-1)[subcategory_index-1]
                if subcategory != assetData['subcategory']:
                    continue
            if search_key_word != "":
                if search_key_word.lower() not in assetData["SearchWords"].lower():
                    continue
            self.filteredAssetDatas.append(assetData)
        self.currentLoadedCardCount = 0
        self.loadItems()
    def reloadItems(self):
        self.clearAllCards()
        self.currentLoadedCardCount = 0
        datas = self.loadItemFromDataBaseAndMakeItAbs()
        self.filteredAssetDatas = []
        for data in datas:
            self.filteredAssetDatas.append(data)
        self.loadItems()
    def addItemCard(self,imagepath:str,name:str,assetID:str):
        index = len(self.cards)
        itemCard = ItemCard(self,index,imagepath,name,assetID)
        itemCard.clicked.connect(self.setSelectedItem)
        itemCard.goToFile.connect(self.goToFile)
        itemCard.deleteItem.connect(self.deleteAsset)
        itemCard.editItem.connect(self.editItem)
        self.cards.append(itemCard)
        self.flowLayout.addWidget(self.cards[index])
    def editItem(self,index:int):
        libraryAssetData = self.filteredAssetDatas[index]
        editInterface = AssetsEditInterface(self.parentWidget().parentWidget().parentWidget().parentWidget())
        editInterface.loadDataFromAsset(libraryAssetData)
        editInterface.show()
    def goToFile(self,index:int):
        libraryAssetData = self.filteredAssetDatas[index]
        os.startfile(os.path.normpath(libraryAssetData["rootFolder"]))
    def deleteAsset(self,index:int):
        libraryAssetData = self.filteredAssetDatas[index]
        w = Dialog("提示",f"是否删除资产{libraryAssetData['name']}?")
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        if w.exec() and Backend.Get().isBackendAvailable():
            ut.removeFolder(libraryAssetData["rootFolder"])
            Backend.Get().deleteAssetFromDB(libraryAssetData["AssetID"])
            self.reloadItems()
        self.assetDelete.emit()
    def exportToUnreal(self):
        if ut.sendAssetToUE(
            self.filteredAssetDatas[self.currentSelectedIndex],
            Config.Get().getSendSocketAddress(),
            self.infoPanel.combox_res.currentIndex(),
            self.infoPanel.combox_lod.currentText()):
            InfoBar.success(
                title=self.tra('Notice:'),
                content=self.tra("Export successful"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            InfoBar.error(
                title=self.tra('Error:'),
                content=self.tra("Export failed"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
    def resizeItemCards(self):
        itemsPerRow = 3
        width = self.flowWidget.width()-2 * self.flowLayoutSideMargins
        if width <= self.initPerItemCardSize:
            width = 685
        if width < 412:
            itemsPerRow = 2
        elif width > 685 and width < 1200:
            itemsPerRow = 4
        elif width > 1200:
            itemsPerRow = 5
        cardSize = round(width/itemsPerRow - 2 * self.perItemSpacing )
        self.setPerCardSize(cardSize)
    def paintEvent(self, a0: QPaintEvent | None) -> None:
        self.resizeItemCards()
        return super().paintEvent(a0)
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        return super().closeEvent(a0)
    


class EidtInterface(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(800,600)


class HomeInterface(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.rootLayout = QVBoxLayout(self)
        self.item_header = ItemHeader(self)
        self.item_card_view = ItemCardView(self)
        self.item_card_view.assetDelete.connect(self.FilterCardsPerLevel)
        self.__initWidget()
        self.__initConnection()
        self.__setQss()
        self.setObjectName("home_interface")

    def __initWidget(self):
        self.rootLayout.addWidget(self.item_header)
        self.rootLayout.addWidget(self.item_card_view)
        self.rootLayout.setContentsMargins(0,0,0,0)

    def __initConnection(self):
        self.item_header.searchSignal.connect(self.FilterCardsPerLevel)
        self.item_header.clearSignal.connect(self.FilterCardsPerLevel)
        self.item_header.combox_type.currentIndexChanged.connect(self.FilterCardsPerLevel)
        self.item_header.combox_category.currentIndexChanged.connect(self.changeSubcategoryComboxBaseOnCategory)
        self.item_header.combox_subcategory.currentIndexChanged.connect(self.FilterCardsPerLevel)
        self.item_card_view.infoPanel.onTagClicked.connect(self.setSearchText)
    def setSearchText(self,text):
        self.item_header.searchBar.setText(text)
        self.FilterCardsPerLevel()
    def FilterCardsPerLevel(self,*arg):
        type_index = self.item_header.combox_type.currentIndex()
        category_index = self.item_header.combox_category.currentIndex()
        subcategory_index = self.item_header.combox_subcategory.currentIndex()
        search_key_word = self.item_header.searchBar.text()
        self.item_card_view.FilterCards(type_index,category_index,subcategory_index,search_key_word)
    #根据主分类改变次级分类
    def changeSubcategoryComboxBaseOnCategory(self,index):
        index = index - 1
        if index >= 0:
            self.item_header.combox_subcategory.clear()
            self.item_header.combox_subcategory.addItem("请选择资产次级分类")
            self.item_header.combox_subcategory.addItems(ut.GetSubCategorys(index))
        else:
            self.item_header.combox_subcategory.clear()
            self.item_header.combox_subcategory.addItem("请选择资产次级分类")

    def __setQss(self):
        StyleSheet.HOME_INTERFACE.apply(self)



        
