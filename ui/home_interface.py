from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,
                            setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,
                            SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,ImageLabel,TitleLabel)
from qfluentwidgets import FluentIcon as FIF


from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QStyleOption,QGraphicsDropShadowEffect)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)
from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve,pyqtSignal


from core.Log import log
from core.style_sheet import StyleSheet
from core.qtUtility import scaleMap





class ItemCard(QFrame):
    clicked = pyqtSignal(int)
    def __init__(self,index:int,parent=None,size:int=250):
        super().__init__(parent=parent)
        self.setFixedSize(size,size)
        self.item_image_path = "image\Kettle.png"
        self.item_name = "Kettle"
        self.__textPaddingX = 5
        self.__textPaddingY = 5
        self.isSelected = False
        self.index = index
    def mouseReleaseEvent(self, e: QMouseEvent | None) -> None:
        if self.isSelected:
            return
        self.clicked.emit(self.index)
    def paintEvent(self, e: QPaintEvent | None) -> None:
        painter = QPainter(self)
        brush = QBrush()
        brush.setTexture(scaleMap(painter.device().width(),painter.device().height(),self.item_image_path))
        rect  = QRect(0,0,painter.device().width(),painter.device().height())
        painter.fillRect(rect,brush)
        painter.drawText(0+self.__textPaddingX,self.height()-self.__textPaddingY,self.item_name)
        painter.end()
    def setSize(self,size:int):
        self.resize(size,size)
        self.setFixedSize(size,size)
    def setSelected(self,isSelected:bool,force=False):
        if isSelected == self.isSelected and not force:
            return
        self.isSelected = isSelected
        self.setProperty("isSelected",self.isSelected)
        self.setStyle(QApplication.style())


class InfoPanel(QFrame):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.setFixedWidth(400)
        self.shadowWidth = 20

        self.rootLayout = QVBoxLayout(self)
        self.titleImage = ImageLabel(scaleMap(self.width(),200,"image\Kettle.png"),self)

        self.titelWidget = QWidget(self)
        self.titelWidgetLayout = QVBoxLayout(self.titelWidget)

        self.titleLabel = TitleLabel("Test",self.titelWidget)




        self.__initWidget()
    def __initWidget(self):
        self.rootLayout.addWidget(self.titleImage,alignment=Qt.AlignTop)
        self.rootLayout.addWidget(self.titelWidget,alignment=Qt.AlignTop)

        self.titelWidget.setObjectName("InfoPanelTitleWidget")
        self.titelWidgetLayout.addWidget(self.titleLabel)

        
class ItemHeader(QFrame):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.rootLayout = QVBoxLayout(self)
        
        self.headerWidget = QWidget(self)
        self.headerWidgetLayout = QVBoxLayout(self.headerWidget)

        self.searchBar = SearchLineEdit(self.headerWidget)


        self.comboxWidget = QWidget(self.headerWidget)
        self.comboxWidgetLayout = QHBoxLayout(self.comboxWidget)

        self.combox1 = ComboBox(self.comboxWidget)
        self.combox1.addItem("Test")
        self.combox1.addItem("Test")
        self.combox1.addItem("Test")

        self.combox2 = ComboBox(self.comboxWidget)
        self.combox2.addItem("Test")
        self.combox2.addItem("Test")
        self.combox2.addItem("Test")

        self.combox3 = ComboBox(self.comboxWidget)
        self.combox3.addItem("Test")
        self.combox3.addItem("Test")
        self.combox3.addItem("Test")

        self.__initWidget()
    def __initWidget(self):
        self.rootLayout.addWidget(self.headerWidget)
        self.rootLayout.setContentsMargins(15,15,15,15)
        self.headerWidgetLayout.addWidget(self.searchBar)
        self.headerWidgetLayout.addWidget(self.comboxWidget)
        self.headerWidgetLayout.setContentsMargins(0,0,0,0)

        self.comboxWidgetLayout.addWidget(self.combox1)
        self.comboxWidgetLayout.addWidget(self.combox2)
        self.comboxWidgetLayout.addWidget(self.combox3)
        self.comboxWidgetLayout.setContentsMargins(0,0,0,0)

class ItemCardView(QWidget):
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
        self.infoPanelLayout = QVBoxLayout(self.infoPanel)

        self.flowWidget = QWidget(self.scrollArea)
        self.flowLayout = FlowLayout(self.flowWidget,False,True)

        # methods
        self.addItemCard()
        self.__initWidget()
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        self.setSelectedItem(-1)
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


        self.flowLayout.setVerticalSpacing(self.perItemSpacing)
        self.flowLayout.setHorizontalSpacing(self.perItemSpacing)
        self.flowLayout.setContentsMargins(self.flowLayoutSideMargins,0,self.flowLayoutSideMargins,0)
        self.flowLayout.setAnimation(250, QEasingCurve.OutQuad)

    def showAllCards(self):
        self.flowLayout.removeAllWidgets()
        for card in self.cards:
            self.flowLayout.addWidget(card)
    def setPerCardSize(self,size):
        for card in self.cards:
            card.setSize(size)
    def addItemCard(self):
        itemCard = ItemCard(len(self.cards),self,self.initPerItemCardSize)
        itemCard.clicked.connect(self.setSelectedItem)
        self.cards.append(itemCard)
    def setSelectedItem(self,index:int):
        #清除当前选择的项目
        self.cards[self.currentSelectedIndex].setSelected(False)
        #如果输入的索引大于0,表示选中了有效的项目,否则说明只是清空项目
        if index >=0:
            self.cards[index].setSelected(True)
        
        self.currentSelectedIndex = index

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
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


class HomeInterface(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.rootLayout = QVBoxLayout(self)
        self.item_header = ItemHeader(self)

        self.item_card_view = ItemCardView(self)
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.addItemCard()
        self.item_card_view.showAllCards()

        self.__initWidget()
        self.__initConnection()
        self.__setQss()
        self.setObjectName("home_interface")

    def __initWidget(self):
        self.rootLayout.addWidget(self.item_header)
        self.rootLayout.addWidget(self.item_card_view)

        self.rootLayout.setContentsMargins(0,0,0,0)
    def __initConnection(self):
        pass
    def __setQss(self):
        StyleSheet.HOME_INTERFACE.apply(self)
        StyleSheet.HOME_INTERFACE.apply(self.item_card_view)
        StyleSheet.HOME_INTERFACE.apply(self.item_header)




        
