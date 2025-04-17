
# coding: utf-8
from qfluentwidgets import NavigationItemPosition,FluentWindow,toggleTheme,SplashScreen
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt
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
        self.__initWindow()
        self.__createSubInterface()

        self.splashScreen.finish()
    def __createSubInterface(self):
        #create sub window
        self.homeInterface = HomeInterface(self)
        self.SettingInterface = SettingInterface(self)
        self.assetImportInterface = AssetsImportInterface(self)
        #add sub interface
        nvaigration = self.addSubInterface(self.homeInterface,FIF.HOME,self.tra("Home"))
        #nvaigration.clicked.connect(lambda:self.homeInterface.item_card_view.reloadItems())
        nvaigration = self.addSubInterface(self.assetImportInterface,FIF.DOWNLOAD,self.tra("Import"))
        nvaigration = self.addSubInterface(self.SettingInterface,FIF.SETTING,self.tra("Settings"),NavigationItemPosition.BOTTOM)
    def __initWindow(self):
        self.setWindowTitle("MyBridge")
        self.setWindowIcon(QIcon(r":/MyBridge/image/icon.ico"))
        self.navigationInterface.setExpandWidth(130)
        self.setMinimumSize(1200,400)
        self.resize(1200,800)

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.splashScreen.raise_()
        
        # move to center
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.show()
        # 立即处理当前事件循环中所有待处理的事件,保持程序响应性.
        # 避免界面冻结,实时更新UI
        QApplication.processEvents()
    def closeEvent(self, e):
        Log("主窗口已经关闭","Main")
        return super().closeEvent(e)
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
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
    



