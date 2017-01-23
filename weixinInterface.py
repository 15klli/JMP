# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import pylibmc # 以使用 Memcached 功能

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

        mc = pylibmc.Client() #初始化一个memcache实例用来保存用户的操作

       # return self.render.reply_text(fromUser,toUser,int(time.time()),u"我是你大爷，"+content) # render方法是按 reply_text.xml 这个模板渲染，传入参数后就转换成微信要求的 XML 内容
        

        if msgType == 'text':
            content = xml.find("Content").text

            if content == u'拾卡':
                reply = u'请你这个叼毛按如下格式提交拾卡信息:\ns+卡号+(空格)+当前所在地\n如：s20481024 你爹床上'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)

            if content.startswith('s'):
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'感谢叼毛的拾卡，我们已经第一时间通知施主了')

            if content == u'不见卡了':
                reply = u'你这个几把又不见卡了？\n马上输入:z+卡号\n如：z9527321'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)

            if content.startswith('z'):
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'如果有人这么倒霉，捡到叼毛的卡，我们也不得不第一时间通知你了')


            # 处理注册

            if content == u'注册':
                mc.set(fromUser+'_register','cardnum') # 注册入口
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'叼毛，我们来注(p)册(y)了，请输入你的学号！\n输入 bye 结束交易')

            if content.lower() == 'bye':
                mc.delete(fromUser+'_register')
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'你大力挣脱了小鞭，交易结束')

            mc_register = mc.get(fromUser+'_register') # 读取 memcached 中的缓存数据

            ## 处理学号
            if mc_register == 'cardnum':
                if content.startswith('20') and ( len(content) == 10):
                    cardnum = add_cardnum(content)
                    mc.set(fromUser+'_register','mail') 
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'已记录你的学号'+cardnum+'！下面来输邮箱，不给就通知不了你啦（祝你丢卡）')
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u'叼毛，你手残输错啦，再来一次吧')

    def add_cardnum(cardnum):
        return cardnum

