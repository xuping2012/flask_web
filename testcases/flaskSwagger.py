'''
Created on 2021年5月24日

@author: qguan
'''
from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse

app = Flask(__name__)
# 接口文档头
api = Api(app, version='1.0', title='Swagger接口文档', description='用户中心',)

# 接口
http = api.namespace('login', description='登录接口')               # 模块命名空间

# 响应参数
todo = api.model('描述', {                               # 返回值模型
  'result': fields.Integer(readonly=True, description='True of False'),
  'token': fields.String(required=True, description='Return Token')
})

# 定义接口参数
parser = reqparse.RequestParser()                      # 参数模型
parser.add_argument('zone', type=str, required=True, help="国别码/区号")
parser.add_argument('mobile', type=str, required=True, help="手机号")
parser.add_argument('code', type=int, required=True, help="验证码")


class TodoDAO(Resource):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = parser.parse_args()

    @http.expect(parser)                  # 用于解析对应文档参数，             
    @http.response(200, "success response", todo)      # 对应解析文档返回值
    def get(self):
        return self.params


http.add_resource(TodoDAO, "/ByMobile", endpoint="to_do")

if __name__ == '__main__':
    app.run(debug=True)