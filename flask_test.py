'''
Created on 2020年11月23日

@author: qguan
'''

from flask import Flask
from flask.json import jsonify

app=Flask(__name__)


@app.route("/helloworld/<name>")
def hello(name):
    
    
    """"""
    return jsonify({"code":1,"result":{"name":"joe","age":19}})

if __name__ == '__main__':
    app.run(debug=True)