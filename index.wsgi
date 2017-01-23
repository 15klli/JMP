# coding: UTF-8
import os

import sae
import web
from weixinInterface import WeixinInterface #导入 WeixinInterface 这个类

urls = (
'/weixin','WeixinInterface'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc() # 这里是“new”出这个 app ？
application = sae.create_wsgi_app(app)	# 创建应用