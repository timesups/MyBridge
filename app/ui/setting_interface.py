from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,TitleLabel,
                            PushSettingCard,SettingCardGroup,SettingCard,
                            LineEdit,InfoBar,InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF


from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QFileDialog)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)
from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve,QStandardPaths,pyqtSignal
from qfluentwidgets.common.icon import FluentIconBase
from app.core.style_sheet import StyleSheet

from app.core.Log import log
from app.core.config import Config
from app.core.translator import Translator

class LineEditSettingCard(SettingCard):
    editingFinished = pyqtSignal(str)
    def __init__(self, icon: str | QIcon | FluentIconBase, title, text=None, parent=None):
        super().__init__(icon, title, None, parent)
        self.text = text
        self.__initWindow()
    def __initWindow(self):
        self.lineEdit = LineEdit(self)
        self.lineEdit.setMinimumWidth(200)
        self.lineEdit.setText(self.text)
        self.hBoxLayout.addWidget(self.lineEdit)
        self.hBoxLayout.addSpacing(16)
        self.lineEdit.editingFinished.connect(self.__editingFinished)
    def setText(self,text:str):
        self.text = text
        self.lineEdit.setText(text)
    def __editingFinished(self):
        text = self.lineEdit.text()
        self.editingFinished.emit(text)


class SettingInterface(QWidget,Translator):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.__initWindow()
        self.__setQss()
    def __initWindow(self):
        rootLayout = QVBoxLayout(self)

        label_Settings = TitleLabel(self.tra("Settings"),self)
        group_path_settings = SettingCardGroup(self.tra("Path Settings"),self)
        self.card_remote_library_path = PushSettingCard(
            self.tra("Choose folder"),
            FIF.LIBRARY_FILL,
            self.tra("Remote Library Directory"),
            Config.Get().remoteAssetLibraryFolder,
            group_path_settings
        )
        self.card_remote_library_path.clicked.connect(self.__SeletLibraryFolder)
        
        group_path_settings.addSettingCard(self.card_remote_library_path)
        group_path_settings.setMaximumHeight(150)

        group_connect_settings = SettingCardGroup(self.tra("Connect Settings"),self)

        card_connect_address = LineEditSettingCard(
            FIF.CONNECT,
            self.tra("Connect address"),
            text = Config.Get().sockeAddress,
            parent = group_connect_settings
        )
        card_connect_address.editingFinished.connect(self.__setAddress)
        card_connect_port = LineEditSettingCard(
            FIF.CONNECT,
            self.tra("Connect port"),
            text = str(Config.Get().socketSendPort),
            parent = group_connect_settings
        )
        card_connect_port.editingFinished.connect(self.__setPort)
        group_connect_settings.addSettingCard(card_connect_address)
        group_connect_settings.addSettingCard(card_connect_port)


        rootLayout.addWidget(label_Settings)
        rootLayout.addWidget(group_path_settings)
        rootLayout.addWidget(group_connect_settings)
        rootLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        

        rootLayout.setContentsMargins(50,30,50,30)
        rootLayout.setSpacing(0)
        self.setObjectName("setting_interface")
    def __SeletLibraryFolder(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.tra("Choose folder"), "./")
        if not folder or Config.Get().remoteAssetLibraryFolder == folder:
            return
        Config.Get().remoteAssetLibraryFolder = folder
        self.card_remote_library_path.setContent(folder)
        Config.Get().saveConfig()
        self.showInfoConfigSaved()
    def __setAddress(self,text:str):
        Config.Get().sockeAddress = text
        Config.Get().saveConfig()
        self.showInfoConfigSaved()
    def __setPort(self,text:str):
        Config.Get().socketSendPort = eval(text)
        Config.Get().saveConfig()
        self.showInfoConfigSaved()
    def showInfoConfigSaved(self):
        InfoBar.success(
            title=self.tra('notice:'),
            content=self.tra("current settings is saved"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    def __setQss(self):
        pass
