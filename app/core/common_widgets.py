from qfluentwidgets import (Dialog,PushButton,IndeterminateProgressRing,SubtitleLabel)
from qfluentwidgets import FluentIcon as FIF


from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QStyleOption)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)
from PyQt5.QtCore import QObject, QRect,Qt,QPoint,QEasingCurve,pyqtSignal,QThread


import sys

def LoadPixmapSafely(path):
    pixmap = QPixmap(path)
    return(pixmap)

class QLine(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFrameShadow(QFrame.Shadow.Sunken)
    def SetHorizontal(self):
        self.setFrameShape(QFrame.Shape.HLine)
    def SetVertical(self):
        self.setFrameShape(QFrame.Shape.VLine)
    @classmethod
    def HLine(cls,parent):
        line = QLine(parent)
        line.SetHorizontal()
        return line
    @classmethod
    def VLine(cls,parent):
        line = QLine(parent)
        line.SetVertical()
        return line

def scaleMap(width:int,height:int,mapPath:str)-> QPixmap:
    original_pixelmap = QPixmap(mapPath)

    scaled_pixmap = QPixmap(width,height)
    scaled_pixmap.fill(QColor(80,80,80,0))


    painter = QPainter(scaled_pixmap)
    
    try:
        scaled_factor = min(width / float(original_pixelmap.width()+0.1), height / float(original_pixelmap.height()+0.1))
    except ZeroDivisionError:
        scaled_factor = 0.3
        pass

    scaled_size = original_pixelmap.size() * scaled_factor

    x = (width - scaled_size.width()) / 2
    y = (height - scaled_size.height()) / 2
    
    painter.drawPixmap(QRect(int(x), int(y), scaled_size.width(), scaled_size.height()), original_pixelmap)

    painter.end()

    return scaled_pixmap


def scalePixelMap(width:int,height:int,original_pixelmap:QPixmap)-> QPixmap:
    scaled_pixmap = QPixmap(width,height)
    scaled_pixmap.fill(QColor(80,80,80,0))

    painter = QPainter(scaled_pixmap)

    try:
        scaled_factor = min(width / float(original_pixelmap.width()+0.1), height / float(original_pixelmap.height()+0.1))
    except ZeroDivisionError:
        scaled_factor = 0.3
        pass
    
    scaled_size = original_pixelmap.size() * scaled_factor

    x = (width - scaled_size.width()) / 2
    y = (height - scaled_size.height()) / 2
    
    painter.drawPixmap(QRect(int(x), int(y), scaled_size.width(), scaled_size.height()), original_pixelmap)

    painter.end()
    return scaled_pixmap

def showDialog(title,content):
    w = Dialog(title,content)
    w.setTitleBarVisible(False)
    w.setContentCopyable(True)
    return(w.exec())

class StringButton(PushButton):
    onClicked = pyqtSignal(str)
    def __init__(self,text,icon=FIF.TAG,parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setIcon(icon)
        self.clicked.connect(lambda:self.onClicked.emit(self.text()))

class CommonWorker(QThread):
    fun = None
    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
    def run(self) -> None:
        if self.fun:
            self.fun()


class TitleProgressRing(QWidget):
    def __init__(self, parent=None, start=True,text=""):
        super().__init__(parent)
        self.progressRing = IndeterminateProgressRing(self,start)
        self.title = SubtitleLabel(text= text,parent=self)
        self.__initUI()
    def __initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.progressRing)
        self.mainLayout.addWidget(self.title,alignment=Qt.AlignmentFlag.AlignTop)


        self.mainLayout.setSpacing(10)
        self.setContentsMargins(0,0,0,0)


        self.setLayout(self.mainLayout)
        self.setFixedSize(200,200)
        pass