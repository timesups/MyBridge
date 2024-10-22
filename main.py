
# coding: utf-8
from qfluentwidgets import NavigationItemPosition,FluentWindow,toggleTheme,SplashScreen,NavigationTreeWidget
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication,QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtNetwork import QLocalSocket,QLocalServer
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
        nvaigration.clicked.connect(lambda:self.homeInterface.item_card_view.searchAssets(""))
        #navi_favorite = NavigationTreeWidget(FIF.HEART,text=self.tra("Favorite"),isSelectable=True,parent=nvaigration)
        #nvaigration.addChild(navi_favorite)
        nvaigration = self.addSubInterface(self.importInterface,FIF.DOWNLOAD,self.tra("Import"))
        nvaigration = self.addSubInterface(self.SettingInterface,FIF.SETTING,self.tra("Settings"),NavigationItemPosition.BOTTOM)
    def __initWindow(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

def startApp():
    serverName = "ServerForSingle"
    socket = QLocalSocket()
    socket.connectToServer(serverName)
    if socket.waitForConnected(200):
        return
    else:
        localServer = QLocalServer()
        localServer.listen(serverName)
    app = QApplication(sys.argv)
    toggleTheme()
    window = MainWindow()
    window.show() 
    localServer.close()
    sys.exit(app.exec_())

if __name__ == "__main__":
    startApp()
    # import os

    # from app.core.bridge_type import bridgeToAsset
    
    # folder = r"O:\Shade\Quixel_Textures\Downloaded\surface"
    # successfulAssetCount = 0
    # allFolderCount = 0
    # for path in os.listdir(folder):
    #     rootFolder = os.path.join(folder,path)
    #     asset = bridgeToAsset(rootFolder)
    #     allFolderCount += 1
    #     if asset:
    #         successfulAssetCount += 1
    # print(successfulAssetCount/allFolderCount)
    # print(successfulAssetCount)
    pass




