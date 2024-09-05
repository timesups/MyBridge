
# coding: utf-8
from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,toggleTheme,NavigationItemPosition)
from qfluentwidgets import FluentIcon as FIF


from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)
from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve


import sys

from core.Log import log

from ui.home_interface import HomeInterface
from ui.setting_interface import SettingInterface



class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.homeInterface = HomeInterface(self)
        self.SettingInterface = SettingInterface(self)
        self.setMinimumSize(1200,400)

        self.__initWindow()
        self.__addSubInterface()
        self.__initNavigationInterface()
    def __addSubInterface(self):
        self.addSubInterface(self.homeInterface,FIF.HOME,"HOME")
        self.addSubInterface(self.SettingInterface,FIF.SETTING,"SETTING",NavigationItemPosition.BOTTOM)
        pass
    def __initNavigationInterface(self):
        pass
    def __initWindow(self):
        self.resize(1200,800)
        self.setWindowTitle("MyBridge")

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    toggleTheme()
    window = MainWindow()
    window.show()
    app.exec()


