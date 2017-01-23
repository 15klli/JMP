# _*_ coding:utf-8 _*_
import web
import web.db
import sae.const

db = web.database(
    dbn='mysql',
    host=sae.const.MYSQL_HOST,
    port=int(sae.const.MYSQL_PORT),
    user=sae.const.MYSQL_USER,
    passwd=sae.const.MYSQL_PASS,
    db=sae.const.MYSQL_DB
)


def addfk(username, fktime, fkcontent):
    return db.insert('fk', user=username, time=fktime, fk_content=fkcontent)


def get_fkcontent():
    return db.select('fk', order='id')


def get_teststr():
    return 'test_success'


def is_rollnum(num):
    return (num.startswith('20')) and (len(num) == 10)

def is_mail(content):
    return content.find('@') > 0   # todo：要用正则式检查的，这里先这样
