'''
Created on 2020年12月11日

@author: qguan
'''

import hashlib
from urllib import parse
import urllib.request
import json
import time
import itchat
from WechatPCAPI import WechatPCAPI
import logging
from queue import Queue
import threading


#腾讯智能闲聊接口
#api接口的链接
url_preffix='https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
#因为接口相应参数有要求，一开始是=我是封装在模块里的，但为了大家方便，就整合到了一起
def setParams(array, key, value):
    array[key] = value
#生成接口的sign签名信息方法，接口参数需要 可参考：https://ai.qq.com/doc/auth.shtml 
def genSignString(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, parse.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()


class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}
        self.url_data = ''
        
    #调用接口并返回内容
    def invoke(self, params):
        self.url_data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(self.url, self.url_data)
        try:
            rsp = urllib.request.urlopen(req)
            str_rsp = rsp.read().decode('utf-8')
            dict_rsp = json.loads(str_rsp)
            return dict_rsp
        except Exception as e:
            return {'ret': -1,"error":"{}".format(e)}
        
        #此方法生成为api接口准备串接所需的请求参数
    def Messagela(self,question):
        self.url = url_preffix
        setParams(self.data, 'app_id', self.app_id)#应用标识
        setParams(self.data, 'app_key', self.app_key)   
        setParams(self.data, 'time_stamp', int(time.time()))#时间戳
        setParams(self.data, 'nonce_str', int(time.time()))#随机字符串
        setParams(self.data, 'question', question)#聊天内容
        setParams(self.data, 'session', '10000')#session
        sign_str = genSignString(self.data)
        setParams(self.data, 'sign', sign_str)#签名
        return self.invoke(self.data)


# 需要自己去https://ai.qq.com/product/nlpchat.shtml注册智能闲聊，获取app_id和app_key,且接入
def getmessage(messageall):
        try:
            Message=AiPlat('2160704725', 'reXx7TmLyZxBOv0C')
            response=Message.Messagela(messageall)
            return response.get('data').get('answer')           
        except Exception as e :
            pass
            

# 
# for i in range(3):
#     print(getmessage("去哪里吃饭"))


logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()


def on_message(message):
    queue_recved_message.put(message)
    

# 消息处理示例 仅供参考
def thread_handle_message(wx_inst):
    i=0
    while True:
        message = queue_recved_message.get()
        # 打印所有好友列表信息
#         print(message)
        if 'msg' in message.get('type'):    # 这里是判断收到的是消息 不是别的响应
            # 获取收到谁的消息
            msg_content = message.get('data').get('msg')
            rep_message=getmessage(msg_content)
            
            from_who = message.get('data').get('from_wxid')
            
            # 获取收到群的消息
            from_chatroom_wxid = message.get('data').get('from_chatroom_wxid')
            from_member_wxid = message.get('data').get('from_member_wxid')
#             from_chatroom_nickname = message.get('data', {}).get('from_chatroom_nickname', '')
            
            # 只回复收到的消息
            send_or_recv = message.get('data').get('send_or_recv')
            
            if from_who and send_or_recv[0] == '0':    # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
                print("第{}句话:{}".format(i,msg_content))
                wx_inst.send_text(from_who, rep_message)
                i+=1
            
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

#主程序
# 使用热启动，不需要多次扫码
# '''如启动失败，可将hotReload=True删掉，这是热启动，再次启动时无需在次扫码，具体情况自行考虑'''
# itchat.auto_login(hotReload=True)#hotReload=True
# itchat.run()
if __name__ == '__main__':
    
    main()