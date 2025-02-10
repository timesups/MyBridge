# coding: utf-8
from qfluentwidgets import (PushButton,SmoothScrollArea,ComboBox,
                            TitleLabel,CheckBox,LineEdit,
                            LineEditButton,IndeterminateProgressRing,
                            InfoBar,InfoBarPosition,FlowLayout,Dialog)
from qframelesswindow import FramelessDialog
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import (QApplication,QWidget,
                             QHBoxLayout,QVBoxLayout,
                             QLabel,QLineEdit,QTabWidget,
                             QFileDialog,QTabBar,QSizePolicy)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent,QPalette)
from PyQt5.QtCore import QObject, QSize,pyqtSignal
from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve,QThread
import functools
import os

import app.core.common_widgets as common
from app.core.translator import Translator


class UnrealAssetImportWindow(FramelessDialog,Translator):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800,600)
        self.setWindowTitle("导入UE资源到库中")

        self.__initUI()
    def __initUI(self):
        self.layout_main = QVBoxLayout(self)

        widget_asset = QWidget(self)
        layout_asset = QHBoxLayout(widget_asset)

        self.lb_asset_image = QLabel(widget_asset)
        self.lb_asset_image.setFixedSize(256,256)

        widget_asset_info = QWidget(widget_asset)
        layout_asset_info = QVBoxLayout(widget_asset_info)


        self.lbe_asset_name = common.LineEidtGroup(widget_asset_info,text="名称")
        self.lbe_asset_tags = common.LineEidtGroup(widget_asset_info,text="标签")
        self.combox_category = common.ComboxGroup(widget_asset_info,self.tra("Category"))
        self.combox_subcategory = common.ComboxGroup(widget_asset_info,self.tra("Subcategory"))

        layout_asset_info.addWidget(self.lbe_asset_name)
        layout_asset_info.addWidget(self.lbe_asset_tags)
        layout_asset_info.addWidget(self.combox_category)
        layout_asset_info.addWidget(self.combox_subcategory)


        layout_asset.addWidget(self.lb_asset_image)
        layout_asset.addWidget(widget_asset_info)

        self.layout_main.addWidget(widget_asset)






