
# coding: utf-8
from qfluentwidgets import NavigationItemPosition,FluentWindow,toggleTheme,SplashScreen
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import sys
import app.resource.resource_rc
from app.core.Log import Log
from app.ui.home_interface import HomeInterface
from app.ui.setting_interface import SettingInterface
from app.ui.import_interface import ImportInterface
from app.core.translator import Translator
import app.core.utility as ut

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
        Log("主窗口已经关闭","Main")
        return super().closeEvent(e)

if __name__ == "__main__":
    if ut.get_pid("MyBridge.exe"):
        Log("已经存在运行的实例,本实例退出","Main")
        sys.exit(-1)
    app = QApplication(sys.argv)
    Log("app创建成功","Main")
    toggleTheme()
    Log("检查更新","Main")
    update = ut.checkUpdate()
    if update:
        Log("用户确认更新,准备开始更新","Main")
        import subprocess
        subprocess.Popen([update])
    else:
        Log("未检测到更新,启动窗口中","Main")
        window = MainWindow()
        window.show()
        Log("程序启动完成","Main")
        sys.exit(app.exec_())





