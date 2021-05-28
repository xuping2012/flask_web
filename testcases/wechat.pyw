# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Software: PyCharm

import hashlib
import urllib
from urllib import parse
import requests
import json
from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading


# 日志收集器
logging.basicConfig(level=logging.INFO)
# 接受消息队列消息
queue_recved_message = Queue()

# 获取消息
def on_message(message):
    queue_recved_message.put(message)

# 腾讯：智能闲聊api地址
robot_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

# 参考：https://ai.qq.com/doc/auth.shtml 接口鉴权sign签名方法
def getReqSign(params:dict):
    """入参+appKey生成签名"""
    uri_str = ''
    for key in sorted(params.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, parse.quote(str(params.get(key)), safe=''))
    sign_str = uri_str + 'app_key=' + params.get('app_key')
    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()

    
class Robot:
    """封装机器人:输入内容,分析并回复"""
    
    def __init__(self, app_id, app_key):
        """创建类属性"""
        self.app_id = app_id
        self.app_key = app_key
        self.url = robot_url
        self.data = {}
    
    
    def invoke_robot(self, params:dict):
        """调动智能闲聊q接口，返回结果"""
        try:
            res = requests.get(self.url, params=params)
        except Exception as e:
            return {'ret':-1, "error":"{}".format(e)}
        else:
            return res.json()
    
    # 调用接口并返回内容
#     def invoke(self, params):
#         self.url_data = urllib.parse.urlencode(params).encode("utf-8")
#         print(self.url_data)
#         req = urllib.request.Request(self.url, self.url_data)
#         try:
#             rsp = urllib.request.urlopen(req)
#             str_rsp = rsp.read().decode('utf-8')
#             dict_rsp = json.loads(str_rsp)
#             return dict_rsp
#         except Exception as e:
#             return {'ret': -1,"error":"{}".format(e)}
        
    def get_answer(self, ask_question):
        """根据内容,调用智能机器人接口,获取响应"""
        self.data['app_id'] = self.app_id    # 应用标识
        self.data['app_key'] = self.app_key   
        self.data['time_stamp'] = int(time.time())    # 时间戳
        self.data['nonce_str'] = int(time.time())    # 随机字符串
        self.data['question'] = ask_question    # 聊天内容
        self.data['session'] = '10000'    # session
        sign_str = getReqSign(self.data)
        self.data['sign'] = sign_str    # 签名
        return self.invoke_robot(self.data)


def getmessage(ask_question):
    """初始化机器人:并提出问题获取回复"""
    robot = Robot('2160704725', 'reXx7TmLyZxBOv0C')
    res = robot.get_answer(ask_question)
    return res.get('data',{}).get('answer',"听不懂你在说什么,等你想清楚了再说!!!")           


# 消息处理示例 仅供参考
def thread_handle_message(wx_inst):
    while True:
        message = queue_recved_message.get()
        # 打印所有好友列表信息
#         print(message)
        if 'msg' in message.get('type'):    # 这里是判断收到的是消息 不是别的响应
            # 获取收到谁的消息
            msg_content = message.get('data').get('msg')
            rep_message = getmessage(msg_content)
            from_who = message.get('data').get('from_wxid')
            
            # 获取收到群的消息
            from_chatroom_wxid = message.get('data').get('from_chatroom_wxid')
            from_member_wxid = message.get('data').get('from_member_wxid')
#             from_chatroom_nickname = message.get('data', {}).get('from_chatroom_nickname', '')
            
            # 只回复收到的消息
            send_or_recv = message.get('data').get('send_or_recv')
            
            if from_who and send_or_recv[0] == '0':    # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
                wx_inst.send_text(from_who, rep_message)
            
            # 收到群聊@我的消息，我就@回复她
            if from_chatroom_wxid and send_or_recv[0] == '0' and "@A是我" in msg_content:
                wx_inst.send_text(to_user=from_chatroom_wxid, msg=rep_message, at_someone=from_member_wxid)
                

def main():
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)
    while not wx_inst.get_myself():
        time.sleep(5)
#     print(wx_inst.get_myself())
    threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()
    time.sleep(10)
    
#     测试向小助手发信息
#     wx_inst.send_text(to_user='filehelper', msg='测试信息')
    
    # time.sleep(1)
    # wx_inst.send_link_card(
    #     to_user='filehelper',
    #     title='博客',
    #     desc='我的博客，红领巾技术分享网站',
    #     target_url='http://www.honglingjin.online/',
    #     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
    # )
    
    # time.sleep(1)
    #
    # wx_inst.send_img(to_user='filehelper', img_abspath=r'C:\Users\Leon\Pictures\1.jpg')
    # time.sleep(1)
    #
    # wx_inst.send_file(to_user='filehelper', file_abspath=r'C:\Users\Leon\Desktop\1.txt')
    # time.sleep(1)
    #
    # wx_inst.send_gif(to_user='filehelper', gif_abspath=r'C:\Users\Leon\Desktop\08.gif')
    # time.sleep(1)
    #
    # wx_inst.send_card(to_user='filehelper', wx_id='gh_6ced1cafca19')

    # 这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
#     wx_inst.get_member_of_chatroom('22941059407@chatroom')

    # 新增@群里的某人的功能
#     wx_inst.send_text(to_user='22941059407@chatroom', msg='test for at someone', at_someone='wxid_6ij99jtd6s4722')

    # 这个是更新所有好友、群、公众号信息的，结果信息也从上面的回调返回
    # wx_inst.update_frinds()


if __name__ == '__main__':
    main()
