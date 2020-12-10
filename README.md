### Flask微框架介绍
- pip install flask
```
Flask是一个使用 Python 编写的轻量级 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2 。Flask使用 BSD 授权。
Flask也被称为 “microframework” ，因为它使用简单的核心，用 extension 增加其他功能。Flask没有默认使用的数据库、窗体验证工具．
```

### Jinja2介绍
```
Jinja2是基于python的模板引擎，功能比较类似于于PHP的smarty，J2ee的Freemarker和velocity。 它能完全支持unicode，并具有集成的沙箱执行环境，应用广泛。jinja2使用BSD授权。
```

### Virtualenv虚拟环境管理
```
优势：隔离系统python环境安装的第三方库所带来与项目受影响的因素
```
- 安装：pip install virtualenv 
- 在项目目录下创建venv目录：virtualenv venv
(--no-site-packages带该参数不会复制系统python环境的第三方库到虚拟环境中来)
- 需要激活venv：win系统下:（项目路径下）venv/Script/activate.bat ; 
- linux系统下:source　/venv/bin/activate
- 退出：deactivate.bat，删除：rmvirtualenv venv；进入虚拟环境(win下没有找到)：workon venv
- 注意：一定要先激活venv环境，然后再安装所需要的库，否则pip install 会安装第三方依赖包到本机系统python环境；
那么对于项目中所需要的库安装，都需要进入项目venv目录下安装即可。

### 如何在开发IDEA工具中使用该环境呢？
- 配置当前项目的python解释器路径，指向项目下的venv/Script/python.exe


### 问题
- 安装：flask_sqlalchemy,使用这个库时报错：ModuleNotFoundError: No module named 'MySQLdb'
- - 解决办法(实际没有安装pymysql)：虚拟环境下安装：mysqlclient
