from PyInstaller.__main__ import run
import os





if __name__ == '__main__':
    readme = os.path.join(os.path.dirname(__file__),"Readme.md")
    versionInfo = os.path.join(os.path.dirname(__file__),"version_info.txt")
    with open(readme,'r',encoding='utf-8') as f:
        lines = f.readlines()
    version = ""
    for line in lines:
        if line.startswith('## v'):
            version = line.replace('## v',"")
    version = version.replace('.',',').strip()
    with open(versionInfo,'r',encoding='utf-8') as f:
        info = f.read()
    newInfo = info.replace('vsinfo',version)
    with open(versionInfo,'w+',encoding='utf-8') as f:
        f.write(newInfo)
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
    opts = [
        'update.py',
        '--windowed',  # GUI应用，不显示控制台
        '--name=update',  # 指定生成的可执行文件的名称
        '--noconfirm',
        "--onefile",
        '--clean',#清理打包过程的临时文件
    ]
    run(opts)
    with open(versionInfo,'w+',encoding='utf-8') as f:
        f.write(info)
