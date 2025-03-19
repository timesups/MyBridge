# MyBridge 资产库更新日志
python版本:3.10.9
使用requirements.txt安装依赖
## v0.0.0.0.1
- 完成基本功能
## v0.0.0.0.2
- 资产导入页面在资产导入过程中添加进度条防止窗口卡住
- 主页搜索框,使用回车键执行搜索
- 修复资产导入页面左侧待导入资产队列当当前导入的资产是队列第一个资产,导入完成后,不会自动选中下一个的问题
- 修复在导入资产后,切换回主页,不更新资产列表的问题
- 在打包时将资源文件打包到exe文件中
- 修正窗口左侧导航栏宽度
- 给软件添加启动页面
## v0.0.0.0.3
- 加载资产多线程优化
- UI效果优化
- 导入资产时检测数据库是否被占用,在占用时等待,防止出现多个实例同时写入数据库的情况
## v0.0.0.0.4
- 在资产卡片上添加右键的功能
- 在资产导入页面,显示预览图
- 防止程序被同时打开多个实例
- 添加植物和贴花分类,及带来的问题
- 修正因为汉化带来的Cobom失效的问题
- 使类别和子类生效
## v0.0.0.0.5
- 导入资产到库后,切换到主页可以刷新资产列表
- 优化导入页面的添加标签的方式
## v0.0.0.0.6
- 添加对EXR格式的支持
- 添加删除资产的功能
## v0.0.0.0.7
- 添加对贴花和植物资产导入UE的支持
- 删除资产时,需要确认
- 添加资产标签后,可以删除某个标签
- 修正资产信息不全时,导入崩溃的问题
## v0.1.8.1
- 采用新的版本号命名,并嵌入版本信息到可执行文件中
- 添加自动更新的功能
## v0.1.9.1
- 资产存储使用相对路径,方便更换资产库目录
- 使资产库可以使用网络路径
- 在添加资产时检查权限
- 修正导入界面不同类型的资产最低需求
- 提升自动识别PBRMax资产时,识别的准确度,优化逻辑
- 修正自动识别时,预览图识别失败的问题
- 在资产浏览节面添加Tag按钮
- 修复筛选资产后,之前选择的资产的索引值大于筛选后所剩下的资产的数量从而导致,数组越界的问题
- 分离数据库和配置类
- 采用新的方法,防止程序多开
## v0.1.9.2
- 更换自动更新的逻辑
- 为程序增加"关于"
## v0.1.9.3
- 优化资产显示页面文字大小
- 分离数据库和配置
- 在同步数据库时,如果远程数据库被占用,那么会等待一段时间后再同步
- 优化导出逻辑,在缺失一些贴图时自动生成
- 添加筛选功能
## v0.1.9.4
- 优化一些EXR的读取问题
- 添加导入到UE时选择LOD的功能
- 使用新的分类模式
- 批量添加Bridge资产到库中
## v0.1.9.5
- 将默认盘改为C盘
- 修复本地不存在配置文件时导致的崩溃问题
## v0.1.9.6
- 修正exr在缩放贴图后无法保存为新的exr的问题,替换为png
- 添加选项设置导出到UE的路径,目前设置为一个固定路径,预计在下个版本添加自定义功能
- 在导出时将资产名称中的空格去除
- 在导出到UE时修复法线贴图丢失的问题,并在当前选择的模型等级没有法线贴图时回退到任意存在的法线贴图上面
- 在缺少粗糙度贴图但存在高光贴图时,使用高光贴图代替粗糙度贴图
- 多级搜索初步
- 添加复制资产ID的功能
## v0.1.9.7
- 修复导出贴图尺寸为8K时,当前贴图没有8k导致的错误,方案是将贴图缩放到8K
## v0.2.0.0
- 前后端分离
- 多级筛选
- 内存优化,HOME页面的Card还需要优化,不过目前应该不会出现内存泄漏问题
- 增加资产修改功能
