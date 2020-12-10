'''
# -*- encoding=utf-8 -*-
Created on 2019年10月23日下午6:20:38
@author: qguan
@file:manager.py

'''
# 导入扩展flask
from flask import Flask, request, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref
from werkzeug.routing import BaseConverter
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


# 表单
# 表单的域
# 验证函数
# 数据库操作
# 动态路由：传入参数指定数据路由，支持int、float、path(/路径这个)，默认的可以认为是str类型
# 支持正则匹配路由，转换正则类
class RegexConverter(BaseConverter):
    '''转换正则匹配的path'''

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# 创建flask应用实例，需要传入__name__，作用是为了确定资源所在的路径
app = Flask(__name__)
# 创建这个正则转换类的对象
app.url_map.converters['regex'] = RegexConverter

app.secret_key = "abc"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vagrant@192.168.2.68:3306/flask_db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 需要继承数据库的模型db.Model
class Role(db.Model):
    # 定义表
    __tablename__ = "roles"
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # 1对多，关系模型：Role和User模型发生了关联，增加一个users属性
    # backref:表示role是User要用的属性
    users = db.relationship('User', backref='role')

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Role: {} {}>'.format(self.name, self.id)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(32), unique=False)
    passwd = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Role: {} {} {} {}>'.format(self.name, self.id, self.email, self.passwd)

"""
MySQL的增删查，反向引用；通过session会话进行操作
db.session.add()
db.session.add_all([1,2])
db.session.delete()
db.session.commit()
"""

# 使用wtf实现表单
'''
自定义表单类
'''


class LoginForm(FlaskForm):
    '''定义一个登录表单的字段信息'''
    username = StringField('用户名：', validators=[DataRequired()])
    password = PasswordField("密码：", validators=[DataRequired()])
    submit = SubmitField("提交")


class RigsterForm(FlaskForm):
    '''定义一个注册表单的字段信息'''
    username = StringField('用户名：', validators=[DataRequired()])
    password = PasswordField("密码：", validators=[DataRequired()])
    password2 = PasswordField(
        "输入密码：", validators=[DataRequired(), EqualTo('password', "密码不一致!")])
    submit = SubmitField("提交")


@app.route('/user/<regex("[0-9]{3}"):user_id>')
def users(user_id):
    return "user is %s" % user_id


@app.route("/login", methods=['GET', 'POST'])
def login_wtf():
    # 创建表单对象
    login_form = LoginForm()
    # 获取请求方法
    if request.method == 'POST':
        # 获取表单输入参数：由表单类定义的参数名与html模板的名字一致
        #         username = request.form.get("username")
        #         password = request.form.get("password")
        #         password2 = request.form.get("password2")
        # WTF 一句话验证表单输入的参数
        if login_form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            uname = User.query.filter_by(name=username).first()
            passwd = User.query.filter_by(passwd=password).first()
            if not uname:
                flash("用户没有注册，请先注册!")
                return redirect(url_for("register_wtf"))
            elif not passwd:
                flash("帐号或密码不正确!")
            else:
                # 返回登录成功页面
                return render_template("success.html", username=username, message="登录")
#         # path地址通过?拼接参数请求的参数通过一下方式获取
#         username = request.args.get("username")
#         return render_template("success.html", username=username)
    # 渲染到html
    return render_template('login_wtf.html', form=login_form)


@app.route("/register", methods=['GET', 'POST'])
def register_wtf():
    # 创建表单对象
    register_form = RigsterForm()
    # 获取请求方法
    if request.method == 'POST':
        # 获取表单输入参数：由表单类定义的参数名与html模板的名字一致
        username = request.form.get("username")
        password = request.form.get("password")
#         password2 = request.form.get("password2")
        # WTF 一句话验证表单输入的参数
        if register_form.validate_on_submit():
            uname = User.query.filter_by(name=username).first()
            if not uname:
                new_user = User(
                    name=username, email="test@test.com", passwd=password, role_id=1)
                db.session.add(new_user)
                db.session.commit()
                # 返回注册成功页面
                return render_template("success.html", username=username, message="注册")
            else:
                flash("该用户名已存在，请重新注册!!!")
        else:
            # flash消息闪现
            flash("账号或密码不正确!")
#     else:
#         # path地址通过?拼接参数请求的参数通过一下方式获取
#         username = request.args.get("username")
#         return render_template("success.html", username=username)

    # 渲染到html
    return render_template('register_wtf.html', form=register_form)


# 定义路由和视图函数
# @app.route装饰器
# 路由限定请求方式，默认get请求，method可以指定请求方法，多个方法使用list表示
# 路由限定请求参数数据类型<动态路由>，验证规则：转换器
# 路由指定的数据类型及参数，需要传输视图函数的参数名保持一致
@app.route("/hello/<int:id>", methods=["POST", "GET"])
def hello(id):
    dic = {"name": 'Flask', "age": 18}
    lis = [1, 2, 3, 4, 5, 6]
    if request.method == "POST":
        return "hello flask,method is POST"
    elif request.method == "GET" and id < 12:
        # 变量与模板渲染的变量名尽量保持一致
        return render_template('hello.html', id=id, dic=dic, lis=lis)
    else:
        return "Hello Flask!"


@app.route("/register_old", methods=["post", "GET"])
def user_register():
    # 获取请求方法
    if request.method == "POST":
        # 获取表单提交的请求参数
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        # 判断参数不能为空
        if not all([username, password, password2]):
            # print("账户或密码不能为空!")
            flash("账户或密码不能为空!")
        elif password != password2:
            # print("密码输入不一致!")
            flash(u"密码输入不一致!")
        else:
            flash(u"注册成功!")
            return render_template("success.html", username=username)
    # get请求html渲染
    return render_template("register.html")


# 启动程序
if __name__ == '__main__':
    # 删除表
    db.drop_all()
    # 创建表
    db.create_all()
    role1 = Role(name='admin')
    role2 = Role(name='guest')
    db.session.add(role1)
    db.session.add(role2)
    db.session.commit()

    user1 = User(
        name='lis', email='lis@hcp.tech', passwd='123456', role_id=role1.id)
    user2 = User(
        name='wang', email='wang@hcp.tech', passwd='123456', role_id=role2.id)
    user3 = User(name='xiaoqi', email='xiaoqi@hcp.tech',
                 passwd='123456', role_id=role2.id)
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # 执行run，flask运行在一个简易的服务器(Flask提供)
    app.run(debug=True)
