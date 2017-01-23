# _*_ coding:utf-8 _*_
def is_rollnum(num):
    return (num.startswith('20')) and (len(num) == 10)

def is_mail(content):
    return content.find('@') > 0   # todo：要用正则式检查的，这里先这样

def is_phonenum(content):
    return content.startswith('1') and (len(content) == 11)  # todo：要用正则式解析

def is_location(content):
    return True
