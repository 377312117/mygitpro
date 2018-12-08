'''
此模块用于配置路由映射函数以及反馈给客户端的视图
'''

import os
from datetime import datetime

from flask import Flask, redirect, render_template, request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from config import *
from models import *



  


@app.errorhandler(404)
def page_not_found(e):
    '''用于无法找到页面时的404提示'''
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    '''用于服务器出现错误时的提示'''
    return render_template('500.html'), 500

@app.route('/01-xhr',methods=['GET','POST'])
def index():
    '''用于查看XMLHttpRequest'''
    if request.method == 'GET':
        return render_template('/01-xhr.html')


@app.route('/server',methods=['GET','POST'])
def server():
    '''用于测试ajax的使用'''
    uname=request.args.get('uname','')
    print('用户名:',uname)
    return '我的第一个AJAX请求'


