from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,
                            setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,
                            SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,ImageLabel,TitleLabel,InfoBar,InfoBarPosition,Dialog,PrimaryPushButton)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QStyleOption,QGraphicsDropShadowEffect,QMenu,
                             QLabel,QSizePolicy)
from PyQt5.QtGui import (QContextMenuEvent, QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)
from PyQt5.QtCore import QEvent, QRect,Qt,QPoint,QEasingCurve,pyqtSignal,QThread

import os

from app.core.Log import log
from app.core.style_sheet import StyleSheet
from app.core.qtUtility import scalePixelMap,scaleMap
import app.core.utility as ut
from app.core.config import Config
from app.core.translator import Translator
from app.core.icons import Icons


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
    def __init__(self,parent,index:int,imagePath:str,name:str,size:int=250):
        super().__init__(parent=parent)
        self.setFixedSize(size,size)
        self.item_pixel_map = QPixmap(imagePath)
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
        actionGoToFile = menu.addAction("打开文件夹")
        actionGoToFile.triggered.connect(lambda :self.goToFile.emit(self.index))

        actionDelete = menu.addAction("删除资产")
        actionDelete.triggered.connect(lambda :self.deleteItem.emit(self.index))
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
        rect  = QRect(self.imageMargin,self.imageMargin,painter.device().width()-2*self.imageMargin,painter.device().height()-2*self.imageMargin)
        if not self.worker.isRunning() and self.worker.image != None:
            brush = QBrush()
            brush.setTexture(self.worker.image)
            painter.fillRect(rect,brush)
        else:
            painter.fillRect(rect,QColor(34,34,34)) 
        if self.isHove:
            painter.drawText(0+self.__textPaddingX,self.height()-self.__textPaddingY,f"{self.item_name}")
            # painter.drawPixmap(self.width()-40,self.height()-40,self.heartPixmap)
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
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.setFixedWidth(400)
        self.shadowWidth = 20

        self.rootLayout = QVBoxLayout(self)

        self.scrollArea = SmoothScrollArea(self)
        self.scrollWidget = QWidget(self.scrollArea)
        self.scrollWidgetLayout = QVBoxLayout(self.scrollWidget)

        self.titleImage = InfoPanelImagePreivew(self)

        self.titelWidget = QWidget(self)
        self.titelWidgetLayout = QVBoxLayout(self.titelWidget)

        self.titleLabel = QLabel(self.titelWidget,text="titleLabel")
        self.typeLabel = QLabel(self.titelWidget,text="typeLabel")
        self.categoryLabel = QLabel(self.titelWidget,text="categoryLabel")
        self.subCategoryLabel = QLabel(self.titelWidget,text="subCategoryLabel")


        self.tagsWidget = QWidget(self)
        self.tagsLayout = FlowLayout(self.tagsWidget)

        self.exportWidget = QWidget(self)
        self.exportWidgetLayout = QHBoxLayout(self.exportWidget)

        self.button_export = PushButton(self.tra("Export"),self.exportWidget)

        self.combox_res = ComboBox(parent=self.exportWidget)
        self.combox_res.addItems([item.value for item in list(ut.TextureSize.__members__.values())])
        self.combox_res.currentIndexChanged.connect(self.__saveConfig)
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
        self.scrollWidgetLayout.addWidget(self.tagsWidget)

        self.scrollWidgetLayout.setContentsMargins(0,0,0,0)
        self.scrollWidgetLayout.setSpacing(0)
        self.scrollWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.exportWidgetLayout.addWidget(self.combox_res)
        self.exportWidgetLayout.addWidget(self.button_export)
        self.exportWidgetLayout.setContentsMargins(0,10,0,10)

        self.titelWidget.setObjectName("InfoPanelTitleWidget")
        self.titelWidgetLayout.addWidget(self.titleLabel)
        self.titelWidgetLayout.addWidget(self.typeLabel)
        self.titelWidgetLayout.addWidget(self.categoryLabel)
        self.titelWidgetLayout.addWidget(self.subCategoryLabel)

        self.button_export.clicked.connect(lambda:self.onExportClicked.emit())

        self.titleLabel.setObjectName("titleLabel")
        self.typeLabel.setObjectName("typeLabel")
        self.categoryLabel.setObjectName("categoryLabel")
        self.subCategoryLabel.setObjectName("subCategoryLabel")

        self.tagsWidget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.tagsWidget.setObjectName("TagWidget")

    def setPanelInfo(self,imagePath:str,name:str,type:str,category:str,subCategory:str):
        self.titleImage.setImgae(imagePath)
        self.titleLabel.setText(name)
        self.typeLabel.setText(type)
        self.categoryLabel.setText(category)
        self.subCategoryLabel.setText(subCategory)

        pass
    def __loadConfig(self):
        self.combox_res.setCurrentIndex(Config.Get().exportTextureSizeIndex)
    def __saveConfig(self,index):
        Config.Get().exportTextureSizeIndex = index
        Config.Get().saveConfig()


        
class ItemHeader(QFrame):
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

        self.__initWidget()
    def __initWidget(self):
        self.rootLayout.addWidget(self.headerWidget)
        self.rootLayout.setContentsMargins(15,15,15,15)
        self.headerWidgetLayout.addWidget(self.searchBar)
        self.headerWidgetLayout.addWidget(self.comboxWidget)
        self.headerWidgetLayout.setContentsMargins(0,0,0,0)

        self.comboxWidgetLayout.setContentsMargins(0,0,0,0)
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

class ItemCardView(QWidget,Translator):
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


        self.scrollArea = SmoothScrollArea(self.view)
        self.infoPanel = InfoPanel(self)

        self.flowWidget = FlowWidget(self.scrollArea)
        self.flowLayout = FlowLayout(self.flowWidget,False,True)
        self.LoadCardCountPerTimes = 30
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
        #清除当前选择的项目
        if len(self.cards) > 0:
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
                self.tra(libraryAssetData["category"]),
                self.tra(libraryAssetData["subcategory"])
                )
            self.infoPanel.show()
        self.currentSelectedIndex = index
    def clearAllCards(self):
        self.flowLayout.removeAllWidgets()
        for card in self.cards:
            card.close()
            del card
        self.cards = []
    def loadItems(self):
        for i in range(self.currentLoadedCardCount,self.currentLoadedCardCount+self.LoadCardCountPerTimes):
            if i < len(self.filteredAssetDatas):
                self.addItemCard(self.filteredAssetDatas[i]["previewFile"],self.filteredAssetDatas[i]["name"])
                self.currentLoadedCardCount+=1
            else:
                return
    def searchAssets(self,keyword:str):
        self.clearAllCards()
        self.currentLoadedCardCount = 0
        datas = self.loadItemFromDataBaseAndMakeItAbs()
        self.filteredAssetDatas = []
        for data in datas:
            pattern = data["name"] + data["AssetID"] + ",".join(data["tags"])
            if keyword.lower() in pattern.lower():
                self.filteredAssetDatas.append(data)
        self.loadItems()
    def loadItemFromDataBaseAndMakeItAbs(self):
        datas = Config.Get().getAllAssets()
        newDatas = []
        for data in datas:
            data["rootFolder"] = os.path.join(Config.Get().remoteAssetLibrary,data["rootFolder"])
            data["previewFile"] = os.path.join(Config.Get().remoteAssetLibrary,data["rootFolder"],data["previewFile"])
            data["jsonUri"] =os.path.join(Config.Get().remoteAssetLibrary,data["rootFolder"],data["jsonUri"])
            newDatas.append(data)
        return newDatas
    def clearSearch(self):
        self.clearAllCards()
        self.currentLoadedCardCount = 0
        self.filteredAssetDatas = self.loadItemFromDataBaseAndMakeItAbs()
        self.loadItems()
    def reloadItems(self):
        self.clearAllCards()
        self.currentLoadedCardCount = 0
        datas = self.loadItemFromDataBaseAndMakeItAbs()
        self.filteredAssetDatas = []
        for data in datas:
            self.filteredAssetDatas.append(data)
        self.loadItems()
    def addItemCard(self,imagepath:str,name:str):
        index = len(self.cards)
        itemCard = ItemCard(self,index,imagepath,name)
        itemCard.clicked.connect(self.setSelectedItem)
        itemCard.goToFile.connect(self.goToFile)
        itemCard.deleteItem.connect(self.deleteAsset)
        self.cards.append(itemCard)
        self.flowLayout.addWidget(self.cards[index])
    def goToFile(self,index:int):
        libraryAssetData = self.filteredAssetDatas[index]
        os.startfile(os.path.normpath(libraryAssetData["rootFolder"]))
    def deleteAsset(self,index:int):
        libraryAssetData = self.filteredAssetDatas[index]
        w = Dialog("提示",f"是否删除资产{libraryAssetData['name']}?")
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        if w.exec():
            ut.removeFolder(libraryAssetData["rootFolder"])
            Config.Get().deleteAssetFromDB(libraryAssetData["AssetID"])
            self.reloadItems()
    def exportToUnreal(self):
        if ut.sendAssetToUE(self.filteredAssetDatas[self.currentSelectedIndex],Config.Get().getSendSocketAddress(),self.infoPanel.combox_res.currentIndex()):
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

class HomeInterface(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.rootLayout = QVBoxLayout(self)
        self.item_header = ItemHeader(self)
        self.item_card_view = ItemCardView(self)
        self.__initWidget()
        self.__initConnection()
        self.__setQss()
        self.setObjectName("home_interface")

    def __initWidget(self):
        self.rootLayout.addWidget(self.item_header)
        self.rootLayout.addWidget(self.item_card_view)
        self.rootLayout.setContentsMargins(0,0,0,0)


    def __initConnection(self):
        self.item_header.searchSignal.connect(self.item_card_view.searchAssets)
        self.item_header.clearSignal.connect(self.item_card_view.clearSearch)
        pass
    def __setQss(self):
        StyleSheet.HOME_INTERFACE.apply(self)



        
