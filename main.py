
# coding: utf-8
from qfluentwidgets import NavigationItemPosition,FluentWindow,toggleTheme,NavigationItemPosition,FluentTranslator
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator,QLocale

import sys

from app.core.Log import log

from app.ui.home_interface import HomeInterface
from app.ui.setting_interface import SettingInterface
from app.ui.import_interface import ImportInterface
from app.core.translator import Translator

class MainWindow(FluentWindow,Translator):
    def __init__(self):
        super().__init__()
        self.homeInterface = HomeInterface(self)
        self.SettingInterface = SettingInterface(self)
        self.importInterface = ImportInterface(self)
        self.setMinimumSize(1200,400)
        self.resize(1200,800)
        self.__initWindow()
        self.__addSubInterface()
        self.__initNavigationInterface()
    def __addSubInterface(self):
        nvaigration = self.addSubInterface(self.homeInterface,FIF.HOME,self.tra("Home"))
        nvaigration.clicked.connect(self.homeInterface.item_card_view.reloadItems)
        nvaigration = self.addSubInterface(self.importInterface,FIF.DOWNLOAD,self.tra("Import"))
        nvaigration = self.addSubInterface(self.SettingInterface,FIF.SETTING,self.tra("Settings"),NavigationItemPosition.BOTTOM)
    def __initNavigationInterface(self):
        pass
    def __initWindow(self):
        self.setWindowTitle("MyBridge")
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

def startApp():
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




