import shutil
import os
import sys


names = ["MyBridge.exe",'_internal']
current_exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__
rootDir = os.path.dirname(current_exe_path)
remoteDir = r"\\192.168.3.252\中影年年文化传媒有限公司\6动画基地\制作中心\地编组\Z_赵存喜\MyBirdge\update"

def deleteOldFiles():
    for name in names:
        path = os.path.join(rootDir,name)
        if os.path.isfile(path):
            os.remove(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
def copyNewFiles():
    for name in names:
        srcPath = os.path.join(remoteDir,name)
        desPath = os.path.join(rootDir,name)
        if os.path.isfile(srcPath) and os.path.exists(srcPath):
            shutil.copy(srcPath,desPath)
        if os.path.isdir(srcPath) and os.path.exists(srcPath):
            shutil.copytree(srcPath,desPath)
def run():
    exePath = os.path.join(rootDir,"MyBridge.exe")
    if not os.path.exists(exePath):
        return
    import subprocess
    subprocess.run([exePath])
    
if __name__ == "__main__":
    deleteOldFiles()
    copyNewFiles()
    run()

