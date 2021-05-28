'''
# -*- encoding=utf-8 -*-
Created on 2020年5月27日下午7:30:31
@author: qguan
@file:flask_books.py

'''

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.secret_key = "abc"
# 数据库配置，关闭数据库跟踪修改
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vagrant@192.168.2.68:3306/flask_db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# tips：需要手动去数据库创建flask_db?

# 创建数据库对象
db = SQLAlchemy(app)

"""
简易版图书管理系统
1、配置数据库
    导入SQLAlchemy扩展
    创建db对象，配置参数
    终端创建数据库(MySQL)
    
2、添加作者和图书模型
    创建模型继承db.Model
    创建表名__tablename__
    创建表字段db.Culomn
    创建表关系引用db.relationship
    创建。。。
    
3、添加数据
    使用session会话
    
4、使用模板显示数据库查询的数据
    查询作者信息传递给模板
    模板中遍历所有作者和书籍
    
5、使用WTF显示表单
    自定义表单
    模板中显示
  secret_key编码问题  
  
6、实现相关的增删逻辑
    增加数据
    删除数据

"""

# 定义作者模型


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # books是给自己author的用的，author是给Book模型用的
    books = db.relationship('Book', backref='author')

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Author: {} {}>'.format(self.id, self.name)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    # repr()方法显示一个可读字符串

    def __repr__(self):
        return '<book: {} {}>'.format(self.author, self.name)


class AuthorForm(FlaskForm):
    author = StringField("作者：", validators=[DataRequired()])
    book = StringField("书籍：", validators=[DataRequired()])
    submit = SubmitField("提交")


@app.route("/add", methods=['GET', 'POST'])
def index():
    #     创建自定义表单类
    author_form = AuthorForm()

    '''
            验证逻辑
        1、调用WTF函数实现验证
        2、验证通过获取数据
        3、判断作者是否存在
        4、如果作者存在，判断书籍是否存在，没有重复书籍就添加，否则报错
        5、如果作者不存在，添加作者和书籍
        6、验证不通过就提示错误信息
    '''
    # 1调用WTF函数实现验证
    if author_form.validate_on_submit():
        # 2验证通过获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data

        author = Author.query.filter_by(name=author_name).first()
        if author:  # 3判断作者是否存在
            # 4如果作者存在，判断书籍是否存在，没有重复书籍就添加，否则报错
            book = Book.query.filter_by(name=book_name).first()
            if book:
                flash("已存在同名书籍")
            else:
                # 没有重复书籍
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except:
                    flash("添加书籍失败")
                    db.session.rollback()
        else:
            # 5如果作者不存在，添加作者和书籍
            try:
                # 先添加作者，获取author_id
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()
                # 再添加书籍
                new_book = Book(name=book_name, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except:
                flash("添加作者/书籍失败")
                db.session.rollback()
    else:
        if request.method == 'POST':
            flash("缺少必要参数")

    authors = Author.query.all()

    return render_template('books.html', authors=authors, form=author_form)


@app.route("/delete_book/<book_id>")
def delete_book(book_id):

    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except:
            flash("删除失败")
            db.session.rollback()
            raise
    else:
        flash("书籍不存在")
    #     authors = Author.query.all()
    # redirect 重定向，传入一个地址，
    # url_for():需要传入视图函数名，返回该视图函数对应的路由地址
    return redirect(url_for("index"))


@app.route("/delete_author/<author_id>")
def delete_author(author_id):

    author = Author.query.get(author_id)

    # 先删除书，再删除作者
    if author:
        try:
            Book.query.filter_by(author_id=author.id).delete()

            db.session.delete(author)
            db.session.commit()
        except:
            flash("删除失败")
            db.session.rollback()
            raise
    else:
        flash("作者不存在")
    #     authors = Author.query.all()
    # redirect 重定向，传入一个地址，
    # url_for():需要传入视图函数名，返回该视图函数对应的路由地址
    return redirect(url_for("index"))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    au1 = Author(name="老王")
    au2 = Author(name="老李")
    db.session.add_all([au1, au2])
    db.session.commit()
    bk1 = Book(name="老王，那些年", author_id=au1.id)
    bk2 = Book(name="老李欺负了寡妇", author_id=au2.id)
    bk3 = Book(name="我读书少，不要骗我", author_id=au1.id)
    db.session.add_all([bk1, bk2, bk3])
    db.session.commit()
    app.run(debug=True)
    pass
