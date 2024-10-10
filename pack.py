from PyInstaller.__main__ import run


if __name__ == '__main__':
    opts = [
        'main.py',
        '--windowed',  # GUI应用，不显示控制台
        '--name=MyBridge',  # 指定生成的可执行文件的名称
        '--add-data=app/ui/home_interface.py;.',
        '--add-data=app/ui/import_interface.py;.',
        '--add-data=app/ui/setting_interface.py;.',
        '--add-data=app/core/common_widget.py;.',
        '--add-data=app/core/config.py;.',
        '--add-data=app/core/Log.py;.',
        '--add-data=app/core/qtUtility.py;.',
        '--add-data=app/core/style_sheet.py;.',
        '--add-data=app/core/tools.py;.',
        '--add-data=app/core/translator.py;.',
        '--add-data=app/core/utility.py;.',
        '--add-data=app/resource/qss;qss',
        '--icon=app/resource/image/icon.ico',  # 如果有图标的话
        '--paths=C:/Users/zhaocunxi/.conda/envs/qfw/Lib/site-packages/qfluentwidgets',
        '--paths=C:/Users/zhaocunxi/.conda/envs/qfw/Lib/site-packages/qfluentwidgets/common',
        '--paths=C:/Users/zhaocunxi/.conda/envs/qfw/Lib/site-packages/PyInstaller',
        '--paths=C:/Users/zhaocunxi/.conda/envs/qfw/Lib/site-packages/numpy',
        '--clean',#清理打包过程的临时文件
    ]
    run(opts)