# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

class WeixinInterface:

    def __init__(self): 
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates') # templates 路径——字符串
        self.render = web.template.render(self.templates_root) # 传入template 路径，渲染（即使用模板）

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr

        # 自己的token
        token="fuckyouass" # 这里改写为在特定微信公众平台里输入的token

        # 字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        # sha1加密算法        

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):        
        str_xml = web.data() # 获得post来的数据
        xml = etree.fromstring(str_xml) # 进行XML解析
        content=xml.find("Content").text # 获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
       # return self.render.reply_text(fromUser,toUser,int(time.time()),u"我是你大爷，"+content) # render方法是按 reply_text.xml 这个模板渲染，传入参数后就转换成微信要求的 XML 内容
        if msgType == 'text':
            content = xml.find("Content").text
            if content == u'拾卡':
                reply = u'请你这个叼毛输入拾卡的卡号'
        return self.render.reply_text(fromUser, toUser, int(time.time()), reply)