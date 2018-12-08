"""
此中包含了所有需要创建的模型类
使用数据库进行管理
"""

# 为密码加密的相关模块
from werkzeug.security import check_password_hash, generate_password_hash

# 使用Flask_Login需要使要验证的实体对象（models.py中的Users对象）继承自UserMixin类
from flask_login import UserMixin

from config import *


class Users(db.Model,UserMixin):
    '''
        用户信息表
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    isActive = db.Column(db.Boolean, default=True)

    def __init__(self, name, age, email,_password):
        # 用于实例对象进行赋值
        self.name = name
        self.age = age
        self.email = email
        self.password= _password

    def __repr__(self):
        return f'<User:{self.name}>'
    
    @property
    def password(self):
        return self._password

    # 定义一个赋值的方法
    @password.setter
    def password(self, rawpwd):
        self._password = generate_password_hash(rawpwd)

    #定义一个验证密码的方法
    def check_password(self, rawpwd):
        return check_password_hash(self.password, rawpwd)



class Students(db.Model):
    '''
        学生信息表
    '''
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(80), unique=True, nullable=False)
    sage = db.Column(db.Integer)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    def __init__(self, sname, sage):
        self.sname = sname
        self.sage = sage

    def __repr__(self):
        return f'<Student:{self.sname}>'


class Teachers(db.Model):
    '''
        老师信息表
    '''
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(80), nullable=False)
    tage = db.Column(db.Integer)
    tbirth = db.Column(db.Date)
    # 增加一个列(外键):引用自course表的外键(表名.属性名)
    c_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __init__(self, tname, tage, tbirth):
        self.tname = tname
        self.tage = tage
        self.tbirth = tbirth

    def __repr__(self):
        return f'<Teacher:{self.tname}>'


class Course(db.Model):
    '''
        课程表
    '''
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(80), nullable=False)
    # 增加关联属性和反向引用关系
    # 关联属性,在course对象中通过那个属性能够得到对应的所有的teacher对象
    # 反向引用:在teacher对象中通过哪个属性能够得到它对应的course
    # backref : 相当于teacher拥有couse属性来指向course
    teachers = db.relationship('Teachers', backref='course', lazy='dynamic')

    def __init__(self, cname):
        self.cname = cname

    def __repr__(self):
        return f'<Course:{self.cname}>'


class Classes(db.Model):
    '''
        班级表
    '''
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(80), nullable=False)
    students = db.relationship('Students', backref='class', lazy='dynamic')

    def __init__(self,cname):
        self.cname = cname

    def __repr__(self):
        return f'<Class:{self.cname}>'
