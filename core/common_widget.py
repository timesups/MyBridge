from PyQt5.QtWidgets import QFrame



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