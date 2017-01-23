# _*_ coding:utf-8 _*_
import time
def  register(weixin,fromUser,toUser,content,reply):
    if content == 'test':
        return weixin.render.reply_text(fromUser, toUser, int(time.time()), reply)
