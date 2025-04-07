
# coding: utf-8
from qfluentwidgets import NavigationItemPosition,FluentWindow,toggleTheme,SplashScreen
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox


import sys
import app.resource.resource_rc
from app.core.Log import Log
from app.ui.home_interface import HomeInterface
from app.ui.setting_interface import SettingInterface
from app.core.translator import Translator
import app.core.utility as ut
from app.core.backend import Backend

from app.ui.assets_import_interface import AssetsImportInterface


import subprocess

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
    def ShowAssetImportInterface(self):
        self.assetImportInterface = AssetsImportInterface(self)
        self.assetImportInterface.show()
    def __createSubInterface(self):
        self.homeInterface = HomeInterface(self)
        self.SettingInterface = SettingInterface(self)
        self.assetImportInterface = AssetsImportInterface(self)

        nvaigration = self.addSubInterface(self.homeInterface,FIF.HOME,self.tra("Home"))
        nvaigration.clicked.connect(lambda:self.homeInterface.item_card_view.reloadItems())
        nvaigration = self.addSubInterface(self.assetImportInterface,FIF.DOWNLOAD,self.tra("Import"))
        nvaigration = self.addSubInterface(self.SettingInterface,FIF.SETTING,self.tra("Settings"),NavigationItemPosition.BOTTOM)
    def __initWindow(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    def closeEvent(self, e):
        Log("主窗口已经关闭","Main")
        return super().closeEvent(e)
    def moveEvent(self, a0):
        try:
            self.assetImportInterface.moveEvent(a0)
        except:
            pass
        return super().moveEvent(a0)
    def resizeEvent(self, e):
        try:
            self.assetImportInterface.resizeEvent(e)
        except:
            pass
        return super().resizeEvent(e)
    def showEvent(self, a0):
        if not ut.checkisBackendRunning():
            Log("后台服务未启动","Main")
        return super().showEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Log("app创建成功","Main")
    # 检查是否存在实例
    if ut.get_pid("MyBridge.exe"):
        Log("已经存在运行的实例,本实例退出","Main")
        sys.exit(0)

    #检查更新
    newest_version = Backend.Get().check_update()
    if newest_version:
        reply = QMessageBox.question(None,"确认","发现新版本,是否更新?")
        if reply == 16384:
            newest_version_path = Backend.Get().download_version(newest_version)
            subprocess.Popen([newest_version_path])
            Log("下载完成,开始更新","main")
            sys.exit(0)
        else:
            pass
        
    # 启动窗口

    toggleTheme()
    window = MainWindow()
    window.show()
    Log("程序启动完成","Main")
    sys.exit(app.exec_())
    



