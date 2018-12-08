'''
此模块用于配置路由映射函数以及反馈给客户端的视图
'''

import os
from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from config import *
from models import *


# 示例
@app.route('/01-file', methods=['GET', 'POST'])
def file_views():
    if request.method == 'GET':
        return render_template('/01-file.html')
    else:
        # 处理上传的文件
        # 1.得到上传的文件
        f = request.files['uimg']
        # 2.将文件保存进指定的目录处
        # 3.或将文件保存进指定的目录处[绝对路径]
        # 获取当前文件所在的目录名
        # 加上上传时间格式化字符串作为文件名,避免重复datetime.now().strftime('%Y%m%d%H%M%S%f')
        # 获取文件扩展名
        ext = f.filename.split('.')[-1]
        filepath = os.path.dirname(__file__) + '/uploads/' + datetime.now().strftime('%Y%m%d%H%M%S%f') + '.' + ext
        print(f'当前文件所在目录的绝对路径为:{filepath}')
        f.save(filepath)
        return 'Save OK'


@app.errorhandler(404)
def page_not_found(e):
    '''用于无法找到页面时的404提示'''
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    '''用于服务器出现错误时的提示'''
    return render_template('500.html'), 500


@app.route('/01-add')
def add_views():
    '''创建Users对象,并插入到数据库中'''
    users = Users('李老师', 25, 'mrli@163.com')
    db.session.add(users)
    db.session.commit()
    return 'OK'


@app.route('/02-register', methods=['POST', 'GET'])
def register():
    '''获取对象注册的信息,存入数据库'''
    if request.method == 'GET':
        return render_template('/02-register.html')
    else:
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        age = int(request.form.get('age', ''))
        reguser = Users(username, age, email)
        db.session.add(reguser)
        db.session.commit()
        return '注册成功'


@app.route('/03-query')
def query_views():
    '''使用db.session.query()方法进行查询'''
    # all()等查询函数返回一个可迭代对象组成的列表,使用for循环或者属性进行取值例如:Users.name
    # query = db.session.query(Users).all()
    # # 具体查询部分列
    # query = db.session.query(Users.name)
    # 年纪大于30的记录,返回一个列表,元素为query中查看内容组成的元组
    # 示例:[('1221',), ('122111',)]
    # 查询id==1
    # query = db.session.query(Users.name).filter(Users.id==1).first()
    # 查询年龄大于30或者id>1
    # query = db.session.query(Users).filter(or_(Users.age>30,Users.id>1)).all()
    # id 在2~4之间的用between,[2,4]中的元素用in_([2,4])
    # query = db.session.query(Users.id).filter(Users.id.between(2,4)).all()
    # 获取users表中过滤前两条数据后的前两条的数据
    # query = db.session.query(Users).limit(2).offset(2).all()
    # query = db.session.query(Users).order_by('age desc,id asc').all()
    # group_by()
    # query = db.session.query(Users.age).group_by(Users.age).all()
    # avg()
    # query = db.session.query(Users.age,func.avg(Users.age).label('avgAge')).group_by('age').all()
    # print(query)

    # 基于Models类进行查询
    users = Users.query.all()
    print(users)
    for u in users:
        print(f'姓名:{u.name},年龄:{u.age},邮箱:{u.email}')
    return 'Query OK'


@app.route('/04-queryall', methods=['POST', 'GET'])
def queryall():
    '''将数据库信息显示在网页中'''
    if request.method == 'GET':
        users = Users.query.all()
        # 此用法用于查询该用户是否存在且密码是否正确
        # result = db.session.query(Users).filter(Users.name == '123456').first()
        # if result and result.check_password('123456'):
        #     print(f'result.check_password:{result.check_password("123456")}')
        return render_template('/04-queryall.html', darams=locals())
    else:
        username = request.form.get('uname', '')
        upassword = request.form.get('upassword', '')
        
        uemail = request.form.get('uemail', '')
        uage = request.form.get('uage', '')
        # 参数取的是字段名,
        user = Users(name=username, email=uemail, age=uage,_password = upassword)
        
        db.session.add(user)
        db.session.commit()
        return redirect('/04-queryall')


@app.route('/05-update', methods=['POST', 'GET'])
def update():
    '''接收前端传递来的参数id
        根据id查询出对应的对象
        将查询出来的对象发送到05-update.html中进行显示
    '''
    if request.method == 'GET':
        id = request.args.get('id')
        user = Users.query.filter_by(id=id).first()
        # 将查询出来额对象发送给模板
        return render_template('/05-update.html', user=user)
    else:
        uid = request.form.get('uid', '')
        username = request.form.get('uname', '')
        uemail = request.form.get('uemail', '')
        uage = request.form.get('uage', '')
        user = Users.query.filter_by(id=uid).first()
        user.name = username
        user.age = uage
        user.email = uemail
        db.session.commit()
        return '修改成功'


@app.route('/06-delete')
def delete():
    id = request.args.get('id')
    user = Users.query.filter_by(id=id).first()
    # 将查询出来的对象删除
    user.isActive = False
    db.session.commit()
    # 重定向匹配的是路由位置
    return redirect('/04-queryall')

@app.route('/07-insertviews', methods=['POST', 'GET'])
def insert_views():
    '''查询增加班级信息'''
    if request.method == 'GET':
        courses = Course.query.all()
        print(locals())
        return render_template('/07-insertviews.html', darams=locals())
    else:
        cname = request.form.get('cname', '')
        course = Course(cname=cname)
        db.session.add(course)
        db.session.commit()
        return redirect('/07-insertviews')

@app.route('/08-regteacher', methods=['POST', 'GET'])
def register_teacher():
    '''查询增加老师信息'''
    if request.method == 'GET':
        teachers = Teachers.query.all()
        print(locals())
        return render_template('/08-regteacher.html', darams=locals())
    else:
        tname = request.form.get('tname', '')
        tbirth = request.form.get('tbirth', '')
        tage = request.form.get('tage', '')
        c_id = request.form.get('c_id', '')
        teacher = Teachers(tname=tname, tage=tage,tbirth=tbirth)
        # 方法1:关联关系不能放在上面()里面
        # teacher.c_id = c_id
        # 方法2:查询id为1的Course的信息
        course = Course.query.filter_by(id=c_id).first()
        teacher.course = course
        db.session.add(teacher)
        db.session.commit()
        return redirect('/08-regteacher')

@app.route('/09-select', methods=['POST', 'GET'])
def selecttea():
    '''将数据库信息显示在网页中'''
    if request.method == 'GET':
        id = request.args.get('id')
        course=Course.query.filter_by(id=id).first()
        teachers = course.teachers.all()
        return render_template('/09-select.html',params=locals())
        # 还未完成

@app.route('/11-register_stu', methods=['POST', 'GET'])
def register_stu():
    '''将数据库信息显示在网页中'''
    if request.method == 'GET':
        list = Classes.query.all()
        print('班级表:',list[0].cname)
        return render_template('/11-register_stu.html',list=list)
    else:
        # 获取前端提交的数据
        sname=request.form.get('sname','')
        sage=request.form.get('sage','')
        class_id=request.form.get('class')
        # 构建Students对象
        stu = Students(sname,sage)
        stu.class_id = class_id
        # 将对象保存进数据库
        db.session.add(stu)
        db.session.commit()
        return redirect('/12-students')

@app.route('/12-students', methods=['POST', 'GET'])
def studentslist():
    '''将数据库信息显示在网页中'''
    if request.method == 'GET':
        list = Students.query.all()
        return render_template('12-students.html',list=list)
      
