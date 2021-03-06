# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2, json
import pylibmc  # 以使用 Memcached 功能
from lxml import etree
import check
import control


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')  # templates 路径——字符串
        self.render = web.template.render(self.templates_root)  # 传入template 路径，渲染（即使用模板）

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr

        # 自己的token
        token = "fuckyouass"  # 这里改写为在特定微信公众平台里输入的token

        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法        

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        reinput_warning = u'叼毛，你手残输错啦，再来一次吧'

        # 接收用户的post，并解析提取
        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        content = xml.find("Content").text  # 获得用户所输入的内容
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text

        mc = pylibmc.Client()  # 初始化一个memcache实例用来保存用户的操作

        # return self.render.reply_text(fromUser,toUser,int(time.time()),u"我是你大爷，"+content) # render方法是按 reply_text.xml 这个模板渲染，传入参数后就转换成微信要求的 XML 内容
        if msgType == 'text':
            content = xml.find("Content").text

            # reply = 'tttess'
            # return self.register(fromUser, toUser, content, reply)

            if content == u'不见卡了':
                reply = u'你这个几把又不见卡了？\n马上输入:z+卡号\n如：z9527321'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)

            if content.startswith('z'):
                reply = u'如果有人这么倒霉，捡到叼毛的卡，我们也不得不第一时间通知你了'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)

            # 处理注册
            if content == u'注册':
                mc.set(fromUser + '_register', 'rollnum')  # 注册入口，下同
                reply = u'叼毛，我们来注(p)册(y)了，请输入你的学号！\n输入 bye 结束交易'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)

            if content.lower() == 'bye':
                mc.delete(fromUser + '_register')
                reply = u'你大力挣脱了小鞭，交易结束'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)

            mc_register = mc.get(fromUser + '_register')  # 读取 memcached 中的缓存数据

            # 注册学号
            if mc_register == 'rollnum':
                if check.is_rollnum(content):
                    # add_cardnum(content) # 加入数据库，这里加注释是避免未完成而产生bug
                    mc.set(fromUser + '_register', 'mail')
                    reply = u'已记录你的学号！下面来输邮箱，不给就通知不了你啦（祝你丢卡）'
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reply)
                else:
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reinput_warning)

            # 注册邮箱
            if mc_register == 'mail':
                if check.is_mail(content):
                    add_phonenum(content) # 加入数据库
                    mc.set(fromUser + '_register', 'phonenum')
                    reply = u'已记录你的邮箱！下面来输手机号，不想给就发”bye“'
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reply)
                else:
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reinput_warning)

            # 注册手机号
            if mc_register == 'phonenum':
                if check.is_phonenum(content):
                    add_phonenum(content) # 加入数据库
                    mc.delete(fromUser + '_register')
                    reply = u'已记录你的手机号！注册完成'
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reply)
                else:
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reinput_warning)

            # 处理拾卡
            if content == u'捡到卡了':
                mc.set(fromUser + '_foundcard', 'foundcard_num')  # 注册入口，下同
                reply = u'请输入卡上的学号！'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)

            mc_foundcard = mc.get(fromUser + '_foundcard')

            if mc_foundcard == 'foundcard_num':
                if check.is_rollnum(content):
                    add_foundcard_num(content)
                    mc.set(fromUser + '_foundcard', 'foundcard_location')
                    reply = u'已记录该学号！请告诉我，你将卡放到哪里了？是不是在你下面'
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reply)
                else:
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reinput_warning)

            if mc_foundcard == 'foundcard_location':
                if check.is_location(content):
                    add_foundcard_location(content)
                    reply = u'感谢叼毛的拾卡，我们已经第一时间通知施主了'
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reply)
                else:
                    return self.render.reply_text(fromUser, toUser, int(time.time()), reinput_warning)


def add_rollnum(rollnum):
    pass

def add_phonenum(phonenum):
    pass

def add_mail(mail):
    pass

def add_foundcard_num(num):
    pass

def add_foundcard_location(content):
    pass

    def register(self, fromUser, toUser, content, reply):
        if content == 'test':
            return self.render.reply_text(fromUser, toUser, int(time.time()), reply)
