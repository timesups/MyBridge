from PyInstaller.__main__ import run
import os
import subprocess
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
    shutil.rmtree("build")
    for file in [version_info_file,installer_file,"MyBridge.spec"]:
        os.remove(file)
if __name__ == '__main__':
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    version = get_version()
    version_info_template = os.path.join(os.path.dirname(__file__),"other/version_info_template.txt")
    with open(version_info_template,'r',encoding='utf-8') as f:
        version_info_template = f.read()
    version_info = version_info_template.replace(version_info_flage,",".join(version))
    with open(version_info_file,'w+',encoding='utf-8') as f:
        f.write(version_info)

    installer_template = os.path.join(os.path.dirname(__file__),"other/installer_template.iss")
    with open(installer_template,'r',encoding='utf-8') as f:
        installer_template = f.read()
    installer_info = f'#define MyAppVersion "{".".join(version)}"\n' + installer_template
    with open(installer_file,'w+',encoding='utf-8') as f:
        f.write(installer_info)

    opts = [
        'main.py',
        '--windowed',  # GUI应用，不显示控制台
        '--name=MyBridge',  # 指定生成的可执行文件的名称
        '--noconfirm',
        '--icon=app/resource/image/icon.ico',  # 如果有图标的话
        '--clean',#清理打包过程的临时文件
        "--version-file=version_info.txt"
    ]
    run(opts)
    subprocess.call(f'"{iscc_exe}" installer_pack.iss',cwd=os.path.dirname(__file__))
    clean()
