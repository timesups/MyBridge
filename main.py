
# coding: utf-8
from qfluentwidgets import NavigationItemPosition,FluentWindow,toggleTheme,SplashScreen,Dialog
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication,QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtNetwork import QLocalSocket,QLocalServer
import os

import app.resource.resource_rc
import sys

from app.core.Log import log
from app.core.config import calculate_md5
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
        nvaigration.clicked.connect(lambda:self.homeInterface.item_card_view.reloadItems())
        nvaigration = self.addSubInterface(self.importInterface,FIF.DOWNLOAD,self.tra("Import"))
        nvaigration = self.addSubInterface(self.SettingInterface,FIF.SETTING,self.tra("Settings"),NavigationItemPosition.BOTTOM)
    def __initWindow(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    def closeEvent(self, e):
        return super().closeEvent(e)

def startServe():
    serverName = "ServerForSingle"
    socket = QLocalSocket()
    socket.connectToServer(serverName)
    if socket.waitForConnected(200):
        return
    else:
        localServer = QLocalServer()
        localServer.listen(serverName)
    return localServer



def startApp():
    localServer = startServe()
    app = QApplication(sys.argv)
    toggleTheme()
    update = checkUpdate()
    if update:
        import subprocess
        subprocess.Popen([update])
    else:
        window = MainWindow()
        window.show() 
        localServer.close()
        sys.exit(app.exec_())

def checkUpdate():
    remoteFile = r"\\192.168.3.252\中影年年文化传媒有限公司\6动画基地\制作中心\地编组\Z_赵存喜\MyBirdge\update\MyBridge.exe"
    current_exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__
    currentDir = os.path.dirname(current_exe_path)
    updateExe = os.path.join(currentDir,"update.exe")
    if os.path.exists(remoteFile) and os.path.exists(updateExe):
        if calculate_md5(remoteFile) != calculate_md5(current_exe_path):
            w = Dialog("提示","有新版本,是否更新")
            w.setTitleBarVisible(False)
            w.setContentCopyable(True)
            if w.exec():
                return updateExe
    return False
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




