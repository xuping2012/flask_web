'''
# -*- encoding=utf-8 -*-
Created on 2020年5月28日下午5:13:13
@author: qguan
@file:file_upload.py

'''
from os import path

from flask import Flask, flash, request, redirect, url_for, render_template, make_response
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flask_script import Manager


app = Flask(__name__)

manager = Manager(app)


@app.route("/")
def index():
    # 下面这个没有任何意义，故意让他变成404
    #     abort(404)
    response = make_response(render_template('welcome.html', title="Welcome"))
    response.set_cookie("username", "who are you!")
    return response


# 定义一个404，如果不存在，会指向这个404页面
@app.errorhandler(404)
def page_not_found(errer):
    return render_template('404.html'), 404


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files.get("file")
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(
            basepath, "static", "uploads", secure_filename(f.filename))
        f.save(upload_path)
        # 原来的写法，上传文件报错：PermissionError: [Errno 13] Permission denied
#         upload_path = path.join(basepath, r"static\uploads")
#         f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('upload_file'))
    return render_template("upload.html")


@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch("**/*.*")
    live_server.serve(open_url=True)


if __name__ == '__main__':
    manager.run()
#     app.run(debug=True)
