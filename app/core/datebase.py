from tinydb import TinyDB,Query
import win32file



def is_used(file_name):
    try:
        vHandle = win32file.CreateFile(file_name,win32file.GENERIC_READ,0,None,win32file.OPEN_EXISTING,win32file.FILE_ATTRIBUTE_NORMAL,None)
        return int(vHandle) == win32file.INVALID_HANDLE_VALUE
    except:
        return True
    finally:
        try:
            win32file.CloseHandle(vHandle)
        except:
            pass


class DataBase():
    instance = None
    isUsed = False
    def __init__(self) -> None:
        pass

    @classmethod
    def Get(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance
    

