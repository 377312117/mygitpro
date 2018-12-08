from flask import Flask, url_for, render_template



# 将当前运行的主程序构建成Flask应用,以便接收用户的请求(request)和响应(response)
app = Flask(__name__)




# @app.route('/'):定义Flask中的路由,主要定义用户的路径
# '/'表示整个网站的根路径

# def index():表示的是匹配上@app.route的路径后的处理程序-视图处理函数(Views),所有的
# 视图处理函数必须要有return一个字符串
@app.route('/')
@app.route('/index')
@app.route('/<int:num>')
@app.route('/index/<int:num>')
def index(num=None):
    if num != None:
        if type(num) is int:
            return f'<h1> 当前页数为:{num}</h1>'
        else:
            return '<h1> 当前页数为1</h1>'
    else:
        return '没有响应'


@app.route('/login')
def login():
    return '欢迎访问登录页面'

# 定义带参数的路由以及视图处理函数
@app.route('/show/<name>')
def show1(name):
    return f'<h1> 传递进来的参数为:{name}</h1>'

# 路径:localhost:5000/show/wangwc/25
@app.route('/show/<name>/<int:num>')
def show2(name,num):
    return f'<h1> 传递进来的参数为:{name},{num}岁</h1>'

# 示例method的设置
@app.route('/method',methods=['POST','GET'])
def method():
    return '这是使用post/get请求提交过来的'


# 示例 反向解析
    # 一般正常解析型,会较为繁琐
@app.route('/admin/login/form/show/<name>/<age>')
def show3(name,age):
    # f 和 r 可以联合使用
    return fr"这是/admin/login/form/show/{name}/{age}路径"
    #  反向解析,相当于超链接

@app.route('/url')
def url():
    # 第一个参数是已经写好的视图处理函数
    url=url_for('show3',name='wangwc',age=35)
    print('反向生成的地址为:'+url)
    return f'<a href="{url}">去往show5</a>'




# 模板的渲染
@app.route('/02_system')
def temp():
    # 渲染02_system.html并响应给客户端
    str = render_template('02_system.html',name='RapWang',age=35)
    print(str)
    return str
    
# 模板的渲染,作业
@app.route('/homework')
def homework():
    # 方法2:渲染homework.html并响应给客户端
    # 若变量较多,可以用字典作为容器,再用关键字取值
    # dic = {
    #     'song' : '绿光',
    #     'write_words':'宝强',
    #     'compose':'乃亮',
    #     'singer':'羽凡'
    # }

    # 方法3:locals将变量收集为字典,html文件可以在该字典中进行取值
    song = '绿光'
    write_words='宝强'
    compose='乃亮'
    singer='羽凡'
    # locals()的作用是将常量收入字典中
    print(locals())
    str = render_template('homework.html',params=locals())
    return str


if __name__ == '__main__':
    # 运行Flask应用(启动Flask服务),默认会在本机开启5000端口,允许使用http://localhost:5000
    # 访问Flask的web应用
    # debug=True,将运行模式更改为调试模式(开发环境中推荐使用True,生产环境必须改为False)
    app.run(debug=True)
    # 可在app.run中添加port参数,host参数 ,可修改端口号,默认为5000

