
# coding: utf-8
from qfluentwidgets import NavigationItemPosition,FluentWindow,toggleTheme,SplashScreen,NavigationTreeWidget
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication,QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import app.resource.resource_rc

import sys

from app.core.Log import log

from app.ui.home_interface import HomeInterface
from app.ui.setting_interface import SettingInterface
from app.ui.import_interface import ImportInterface
from app.core.translator import Translator

class MainWindow(FluentWindow,Translator):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyBridge")
        self.setWindowIcon(QIcon(r":/MyBridge/image/icon.ico"))
        self.navigationInterface.setExpandWidth(130)
        self.setMinimumSize(1200,400)
        self.resize(1200,800)
        self.__initWindow()


        self.splashScreen = SplashScreen(self.windowIcon(),self)
        self.splashScreen.setIconSize(QSize(102,102))

        self.show()

        self.__createSubInterface()

        self.splashScreen.finish()

    def __createSubInterface(self):
        self.homeInterface = HomeInterface(self)
        self.SettingInterface = SettingInterface(self)
        self.importInterface = ImportInterface(self)
        nvaigration = self.addSubInterface(self.homeInterface,FIF.HOME,self.tra("Home"))
        #nvaigration.clicked.connect(self.homeInterface.item_card_view.reloadItems)
        #navi_favorite = NavigationTreeWidget(FIF.HEART,text=self.tra("Favorite"),isSelectable=True,parent=nvaigration)
        #nvaigration.addChild(navi_favorite)
        nvaigration = self.addSubInterface(self.importInterface,FIF.DOWNLOAD,self.tra("Import"))
        nvaigration = self.addSubInterface(self.SettingInterface,FIF.SETTING,self.tra("Settings"),NavigationItemPosition.BOTTOM)
    def __initWindow(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

def startApp():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    toggleTheme()
    window = MainWindow()
    window.show() 
    sys.exit(app.exec_())

if __name__ == "__main__":
    # from core.utility import sendCodeToUE
    # from core.config import Config
    # print(sendCodeToUE( 'print("Hello World")',(Config.Get().sockeAddress,Config.Get().socketSendPort)))
    startApp()
    pass




