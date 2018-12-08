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


@app.route('/login',methods=['GET','POST'])
def login():
    '''用于登录'''
    if request.method == 'GET':
        return render_template('/login.html')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        username = request.form.get('username','')
        upassword = request.form.get('upassword','')
        print(f'用户名:{username},用户密码:{upassword}')
        result = db.session.query(Users).filter(Users.name == username).first()
        print('结果是:',result.check_password(upassword))
        if result and result.check_password(upassword):
            return '登陆成功'
        else:
            return '出现异常'

@app.route('/register',methods=['GET','POST'])
def register():
    '''用于注册'''
    if request.method == 'GET':
        return render_template('/login.html')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        username = request.form.get('username','')
        upassword = request.form.get('upassword','')
        repassword = request.form.get('repassword','')
        phonenumber = request.form.get('phonenumber','')
        uemail = request.form.get('uemail','')
        result = db.session.query(Users).filter(Users.name == username,Users.phonenumber == phonenumber).first()
        if result :
            return '已注册,不可重复注册'
        else:
            user = Users(name=username, email=uemail, phonenumber=phonenumber,password = upassword)
            db.session.add(user)
            db.session.commit()
            return '恭喜你,注册成功'


@app.route('/01-users-good')
def users_goods_views():
    # 为1号用户购买1号商品
    user = Users.query.filter_by(id=1).first()
    good = Goods.query.filter_by(id=1).first()
    # 将good商品增加到user的购物列表中
    user.goods.append(good)
    # 将user更新回数据库
    db.session.add(user)
    return 'OK'
    # 

@app.route('/02-remove')
def remove_goods():
    # 移除相关的商品
    user = Users.query.filter_by(id=1).first()
    good = Goods.query.filter_by(id=1).first()
    # 将good从user中移除出去
    user.goods.remove(good)
    return 'Remove OK'

@app.route('/03-query')
def query_goods():
    #查询相关的商品
    user = Users.query.filter_by(id=1).first()
    print('购买者名字:',user.name)
    goods =user.goods.all()
    for g in goods:
        print('商品名称:',g.gname)
        # 通过关联属性来获取该商品的数量
        count = user.UsersGoods.filter_by(goods_id=g.id).first()
        print('购买数量:',count.count)
        
    good = Goods.query.filter_by(gname='苹果').first()
    users=good.users.all()
    for u in users:
        print('购买苹果的用户名称:',u.name)
        # 通过在Goods类中的关联属性来获取该商品的数量
        count = good.goodusers.filter_by(users_id=u.id).first().count
        print('购买苹果的用户购买数量:',count)
    return 'query OK'


@app.route('/04-setCookies')
def setcookie():
    resp = make_response('保存cookie成功')
    # 保存uname 进cookie,值为wangwc
    resp.set_cookie('uname','wangwc',3600)
    return resp

@app.route('/05-getcookies')
def getcookie():
    print(f'cookie中的uname:{request.cookies.get("uname")}')
    return '成功获取所有cookie'


@app.route('/05-delcookies')
def delcookie():
    resp = make_response('删除cookie成功')
    # 保存uname 进cookie,值为wangwc
    resp.delete_cookie('uname')
    return resp


# 此例演示记住密码是如何使用的
@app.route('/06-remember',methods=['GET','POST'])
def remember():
    if request.method == 'GET':
        uname =request.cookies.get("uname")
        upassword = request.cookies.get("upassword")
        if uname == 'admin' and upassword == 'admin':
            return '登录成功'
        else:
            return render_template('/login.html')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        username = request.form.get('username','')
        upassword = request.form.get('upassword','')
        print(f'用户名:{username},用户密码:{upassword}')
        if username == 'admin' and upassword == 'admin':
            # 下法是用于获取checkbox的值,只有一个选项用get,多个选项用getlist
            remember = request.values.get('check')
            print('remember:',remember)
            if remember:
                resp = make_response('保存cookie成功,记住密码')
            # 保存uname 进cookie,值为wangwc
                resp.set_cookie('uname',username,7200)
                resp.set_cookie('upassword',upassword,7200)
                return resp
            else:
                return '未记住密码,登录成功'
        else:
            print('登录失败')
            return redirect('/06-remember')

@app.route('/07-setsession')
def setsession():
    session['uname'] = 'Tarena'
    return '保存session成功'

@app.route('/08-getsession')
def getsession():
    if 'uname' in session:
        uname = session['uname']
        return 'uname:'+uname
    else:
        return 'session中没有相应数据'


