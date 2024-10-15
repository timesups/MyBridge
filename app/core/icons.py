
from app.core.qtUtility import scalePixelMap,scaleMap


class Icons():
    instance = None
    def __init__(self) -> None:
        self.heart = scaleMap(32,32,r":/MyBridge/icons/heart.png")
        self.heartField = scaleMap(32,32,r":/MyBridge/icons/heart_filled.png")
        pass
    @classmethod
    def get(cls):
        if cls.instance == None:
            cls.instance = cls()
        return cls.instance
