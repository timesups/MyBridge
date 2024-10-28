from PyInstaller.__main__ import run


if __name__ == '__main__':
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