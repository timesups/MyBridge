from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,
                            setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,
                            SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,ImageLabel,TitleLabel,InfoBar,InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QStyleOption,QGraphicsDropShadowEffect,QMenu,
                             QLabel)
from PyQt5.QtGui import (QContextMenuEvent, QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)
from PyQt5.QtCore import QEvent, QRect,Qt,QPoint,QEasingCurve,pyqtSignal

import os

from app.core.Log import log
from app.core.style_sheet import StyleSheet
from app.core.qtUtility import scalePixelMap,scaleMap
import app.core.utility as ut
from app.core.config import Config
from app.core.translator import Translator

class ItemCardContextMenu(QMenu):
    def __init__(self,parent=None):
        super().__init__(parent)

class ItemCard(QFrame):
    clicked = pyqtSignal(int)
    goToFile = pyqtSignal(int)
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
        # menu = ItemCardContextMenu(self)
        # actionGoToFile = menu.addAction("go to file")
        # actionGoToFile.triggered.connect(lambda :self.goToFile.emit(self.index))
        # menu.exec_(self.mapToGlobal(self.geometry().center()))
        pass
    def enterEvent(self, a0: QEvent | None) -> None:
        self.isHove = True
        return super().enterEvent(a0)
    def leaveEvent(self, a0: QEvent | None) -> None:
        self.isHove = False
        return super().leaveEvent(a0)
    def mouseReleaseEvent(self, e: QMouseEvent | None) -> None:
        if self.isSelected:
            return
        self.clicked.emit(self.index)
    def paintEvent(self, e: QPaintEvent | None) -> None:
        painter = QPainter(self)
        brush = QBrush()
        brush.setTexture(scalePixelMap(self.width()-2*self.imageMargin,self.height()-2*self.imageMargin,self.item_pixel_map))
        rect  = QRect(self.imageMargin,self.imageMargin,painter.device().width()-2*self.imageMargin,painter.device().height()-2*self.imageMargin)
        painter.fillRect(rect,brush)
        if self.isHove:
            painter.drawText(0+self.__textPaddingX,self.height()-self.__textPaddingY,self.item_name)
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

        self.titleLabel = QLabel(self.titelWidget,text="Test")
        self.typeLabel = QLabel(self.titelWidget,text="Test")

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
        self.scrollWidgetLayout.setContentsMargins(0,0,0,0)
        self.scrollWidgetLayout.setSpacing(0)
        self.scrollWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.exportWidgetLayout.addWidget(self.combox_res)
        self.exportWidgetLayout.addWidget(self.button_export)
        self.exportWidgetLayout.setContentsMargins(0,10,0,10)

        self.titelWidget.setObjectName("InfoPanelTitleWidget")
        self.titelWidgetLayout.addWidget(self.titleLabel)
        self.titelWidgetLayout.addWidget(self.typeLabel)

        self.button_export.clicked.connect(lambda:self.onExportClicked.emit())

        self.titleLabel.setObjectName("titleLabel")
        self.typeLabel.setObjectName("typeLabel")
        
    def setPanelInfo(self,imagePath:str,name:str,type:str):
        self.titleImage.setImgae(imagePath)
        self.titleLabel.setText(name)
        self.typeLabel.setText(type)
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
    clicked = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent=parent)
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        self.clicked.emit()

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


        self.flowWidget.setObjectName("flowwidget")
        self.flowWidget.clicked.connect(lambda: self.setSelectedItem(-1))

        self.infoPanel.onExportClicked.connect(self.exportToUnreal)


        self.flowLayout.setVerticalSpacing(self.perItemSpacing)
        self.flowLayout.setHorizontalSpacing(self.perItemSpacing)
        self.flowLayout.setContentsMargins(self.flowLayoutSideMargins,0,self.flowLayoutSideMargins,0)
        self.flowLayout.setAnimation(250, QEasingCurve.OutQuad)

        # 默认关闭信息面板
        self.infoPanel.close()
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
            libraryAssetData = self.libraryAssetDatas[index]
            self.cards[index].setSelected(True)
            self.infoPanel.setPanelInfo(libraryAssetData["previewFile"],libraryAssetData["name"],libraryAssetData["type"])
            self.infoPanel.show()
        self.currentSelectedIndex = index
    def clearAllCards(self):
        self.flowLayout.removeAllWidgets()
        for card in self.cards:
            card.close()
            del card
        self.cards = []
    def loadItems(self):
        self.libraryAssetDatas = Config.Get().getAllAssets()
        for libraryAssetData in self.libraryAssetDatas:
            self.addItemCard(libraryAssetData["previewFile"],libraryAssetData["name"])
    def searchAssets(self,keyword:str):
        self.setAllCardsHidden(False)
        for i in range(len(self.cards)):
            asset = self.libraryAssetDatas[i]
            pattern = asset["name"] + asset["AssetID"] + ",".join(asset["tags"])
            if keyword.lower() in pattern.lower():
                continue
            self.cards[i].setHidden(True)
    def clearSearch(self):
        self.setAllCardsHidden(False)
    def setAllCardsHidden(self,hidden:bool):
        for i in range(len(self.cards)):
            self.cards[i].setHidden(False)
    def reloadItems(self):
        self.clearAllCards()
        self.loadItems()
    def addItemCard(self,imagepath:str,name:str):
        index = len(self.cards)
        itemCard = ItemCard(self,index,imagepath,name)
        itemCard.clicked.connect(self.setSelectedItem)
        itemCard.goToFile.connect(self.goToFile)
        self.cards.append(itemCard)
        self.flowLayout.addWidget(self.cards[index])
    def goToFile(self,index:int):
        libraryAssetData = self.libraryAssetDatas[index]
        os.startfile(libraryAssetData["rootFolder"])
    def exportToUnreal(self):
        if ut.sendAssetToUE(self.libraryAssetDatas[self.currentSelectedIndex],Config.Get().getSendSocketAddress(),self.infoPanel.combox_res.currentIndex()):
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



        