import sys
ISPACKED = getattr(sys,'frozen',False)

def update_rc_file():
    from app.core.Log import Log
    Log("当前环境:开发,编译qrc文件为py文件","app")
    import os
    qrc_file = r'app\resource\resource.qrc'
    output_file = r'app\resource\resource_rc.py'
    cmd = f'pyrcc5 {qrc_file} -o {output_file}'
    os.system(cmd)



if not ISPACKED:
    update_rc_file()