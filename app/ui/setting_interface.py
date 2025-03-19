from qfluentwidgets import (PrimaryPushSettingCard,TitleLabel,
                            PushSettingCard,SettingCardGroup,SettingCard,
                            LineEdit,InfoBar,InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF

from PyQt5.QtWidgets import (QWidget,QFileDialog,QVBoxLayout)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import Qt,pyqtSignal
from qfluentwidgets.common.icon import FluentIconBase
import functools


import app.core.ImportBridgeAsset as ib
from app.core.Log import Log
from app.core.config import Config
from app.core.translator import Translator
import app.core.utility as ut

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
        group_server_settings = SettingCardGroup(self.tra("服务器设置"),self)
        self.card_server_address = LineEditSettingCard(
            FIF.CONNECT,
            self.tra("服务器地址"),
            text = Config.Get().backendAddress,
            parent = group_server_settings
        )
        self.card_server_address.editingFinished.connect(self.__setBackendAddress)


        version = ""
        exePath = ut.GetExePath()
        if exePath:
            version = ut.getExeVersion(exePath)

        self.aboutGroup = SettingCardGroup("关于", self)
        self.aboutCard = PrimaryPushSettingCard(
            self.tr(''),
            FIF.INFO,
            self.tr('About'),
            '© ' + self.tr('Copyright') + f"  2024,ZCX. " +
            self.tr('Version') + " " + version,
            self.aboutGroup
        )
        self.aboutCard.button.setHidden(True)
        self.aboutGroup.addSettingCard(self.aboutCard)

        
        group_server_settings.addSettingCard(self.card_server_address)
        group_server_settings.setMaximumHeight(150)

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
        rootLayout.addWidget(group_server_settings)
        rootLayout.addWidget(group_connect_settings)
        rootLayout.addWidget(self.aboutGroup)
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
        self.card_server_address.setContent(folder)
        Config.Get().saveConfig()
        self.showInfoConfigSaved()
    def __setAddress(self,text:str):
        Config.Get().sockeAddress = text
        Config.Get().saveConfig()
        self.showInfoConfigSaved()
    def __setBackendAddress(self,text:str):
        Config.Get().backendAddress = text
        Config.Get().saveConfig()
        self.showInfoConfigSaved()
    def __setPort(self,text:str):
        Config.Get().socketSendPort = eval(text)
        Config.Get().saveConfig()
        self.showInfoConfigSaved()
    def showInfoConfigSaved(self):
        InfoBar.success(
            title=self.tra('notice:'),
            content=self.tra("The current Settings have been saved and will take effect after the restart"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    def __setQss(self):
        pass
