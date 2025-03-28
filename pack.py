import os
import sys
import shutil

version_info_flage = "vsinfo"
version_info_file = "version_info.txt"
installer_file = "installer_pack.iss"
iscc_exe = "D:\Program Files (x86)\Inno Setup 6\ISCC.exe"

def get_version():
    readme = os.path.join(os.path.dirname(__file__),"Readme.md")
    with open(readme,'r',encoding='utf-8') as f:
        lines = f.readlines()
    version = ""
    for line in lines:
        if line.startswith('## v'):
            version = line.replace('## v',"")
    version = version.strip().split(".")
    return version

def clean():
    for folder in ["build"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    for file in [version_info_file,installer_file,"MyBridge.spec"]:
        if os.path.exists(file):
            os.remove(file)


def pack_mybridge_by_pyinstaller(debug=False):
    from PyInstaller.__main__ import run
    version = get_version()
    version_info_template = os.path.join(os.path.dirname(__file__),"other/version_info_template.txt")
    with open(version_info_template,'r',encoding='utf-8') as f:
        version_info_template = f.read()
    version_info = version_info_template.replace(version_info_flage,",".join(version))
    with open(version_info_file,'w+',encoding='utf-8') as f:
        f.write(version_info)
    opts = [
        'main.py',
        '--name=MyBridge',  # 指定生成的可执行文件的名称
        '--noconfirm',
        '--icon=app/resource/image/icon.ico',  # 如果有图标的话
        '--clean',#清理打包过程的临时文件
        "--version-file=version_info.txt"
    ]
    #在Debug模式下添加控制台
    if not debug:
        opts.append('--windowed')# GUI应用，不显示控制台
    run(opts)
def pack_mybridge_by_cz_freeze(debug=False):
    from cx_Freeze import setup,Executable
    version = get_version()
    build_exe_options = {
        "packages":[],# 需要额外包含的包
        "excludes":[],# 需要排除的包
        "include_files": [] # 包含的非python文件
    }

    executables = [Executable("main.py",base=None)]

    setup(
        name="MyBridge",
        version = ".".join(version),
        description="MyBridge Description",
        options = {'build_exe':build_exe_options},
        executables = executables
    )
def pack_instaaller():
    import subprocess
    version = get_version()
    installer_template = os.path.join(os.path.dirname(__file__),"other/installer_template.iss")
    with open(installer_template,'r',encoding='utf-8') as f:
        installer_template = f.read()
    installer_info = f'#define MyAppVersion "{".".join(version)}"\n' + installer_template
    with open(installer_file,'w+',encoding='utf-8') as f:
        f.write(installer_info)
    subprocess.call(f'"{iscc_exe}" installer_pack.iss',cwd=os.path.dirname(__file__))


if __name__ == '__main__':
    debug = False
    if "-debug" in sys.argv:
        debug = True
    #清理上次生成的内容
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    #打包软件
    pack_mybridge_by_pyinstaller(debug)

    if not debug:
        #在非Debug模式下打包安装包
        pack_instaaller()
    #执行清理
    clean()
