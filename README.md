### 起因
起初，我每次修改完webapp都需要将它们进行打包，并交给测试去测试程序。这一步骤，我都是小心翼翼的手动挑拣相关的文件和目录并将它们打包在同一个文件夹里，效率极低并且也可能漏了某个相关文件，造成程序无法正常运行的情况。因此，抽时间造了个轮子，简化自己每次打包的操作，提升生产力。

### 目的
帮你简化打包项目的操作，无需手动选择目标文件或者目录，来回复制和粘贴。通过简易配置`project_data.json`，程序即可自动打包。

### 安装
`pip install pypiwin32`

### 配置project_data.json
- projectName：项目名，若不指定，默认为：sourceDir目录名
- projectVersion：项目版本，若不指定，默认为：`项目dll版本`
- releaseDate：发行日期，若不指定，默认为：当前时间
- dateFormat：日期格式，默认为：%Y%m%d (比如：20170304)
- sourceDir：需要打包的目录路径，默认为空，可通过命令行参数传入
- sourceBin：Build项目bin文件夹名
- targetDir：默认在桌面生产打包目录，可指定其它路径
- targetName：生成打包目录的名称，默认为：`projectName_projectVersion_releaseDate`
- packageTask：进行打包的相关任务
    - excludeDir：不打包的目录
    - excludeFile：不打包的文件
    - excludeSuffix：不打包的文件后缀
    - newFile：在打包目录里创建文件，默认创建测试文档。

注意：有关路径的分隔符为：`\\`

### 首次运行
1. 运行register.py，快速生成start.bat和package.reg
2. 双击注册package.reg，添加鼠标右键文件夹菜单：Package Project