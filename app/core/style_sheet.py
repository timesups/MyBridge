# coding: utf-8

from enum import Enum


from qfluentwidgets import StyleSheetBase,Theme,isDarkTheme,qconfig
from PyQt5.QtCore import QFile


class StyleSheet(StyleSheetBase,Enum):
    HOME_INTERFACE = "home_interface"
    IMPORT_INTERFACE = "import_interface"
    SETTING_INTERFACE = "setting_interface"
    CARD_VIEW = "card_view"
    
    def path(self,theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/MyBridge/qss/{theme.value.lower()}/{self.value}.qss"
    
    @classmethod
    def apply_other(cls,fileName:str,widget):
        theme=Theme.AUTO
        theme = qconfig.theme if theme == Theme.AUTO else theme
        path = f":/MyBridge/qss/dark/{fileName}.qss"

        f = QFile(path)
        f.open(QFile.ReadOnly)
        qss = str(f.readAll(), encoding='utf-8')
        f.close()
        widget.setStyleSheet(qss)