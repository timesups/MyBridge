from qfluentwidgets import (NavigationItemPosition,FluentWindow,SubtitleLabel,setFont,SplitFluentWindow,setTheme,
                            Theme,FlowLayout,PushButton,SmoothScrollArea,applyThemeColor,SearchLineEdit,
                            ComboBox,NavigationTreeWidget,ImageLabel,TitleLabel,LineEdit,LineEditButton)
from qfluentwidgets import FluentIcon as FIF


from PyQt5.QtWidgets import (QApplication,QWidget,QScrollArea,
                             QFrame,QHBoxLayout,QVBoxLayout,
                             QAction,QStyleOption)
from PyQt5.QtGui import (QIcon, QMouseEvent, QPaintEvent,
                         QBrush,QPainter,QImage,QPixmap,QColor, 
                         QResizeEvent)
from PyQt5.QtCore import QRect,Qt,QPoint,QEasingCurve,pyqtSignal




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