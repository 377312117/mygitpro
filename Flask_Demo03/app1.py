from flask import Flask,url_for,render_template,request

# 将当前运行的主程序构建成Flask应用,以便接收用户的请求(request)和响应(response)
app = Flask(__name__)


@app.route('/01-parent')
def parent():
    return render_template('01-parent.html')


@app.route('/02-child')
def child():
    return render_template('02-child.html')

@app.route('/03-request')
def request_views():
    # 获取请求的方案(协议)
    scheme = request.scheme
    # 获取请求方式
    method = request.method
    #获取使用get方式提交过来的数据
    args = request.args 
    # 获取post请求的数据
    form = request.form 
    # 获取cookies中的数据
    cookies = request.cookies
    # 获取所有的请求消息头
    headers = request.headers
    # 获取请求资源的路径,不带参数
    path = request.path
    # 获取请求资源的路径,带参数
    full_path= request.full_path
    # 获取请求路径
    url = request.url
    # 获取具体的请求消息头
    referer=request.headers.get('Referer','/')
    ua = request.headers['User-Agent']

    dir1 = dir(request) 
    return render_template('03-request.html',params=locals())

@app.route('/04-form')
def form():
    return render_template('04-form.html')

@app.route('/05-get',methods=['POST','GET'])
def get():
    # 接收04-form.html 传递过来的数据
    if request.method == 'GET':
        uname = request.args.get('uname','')
        upwd = request.args.get('upwd','')
    elif request.method == 'POST':
        uname = request.form.get('uname','')
        upwd = request.form.get('upwd','')
    return f'<h2>用户名:{uname},密码:{upwd}'

@app.route('/05-form')
def formget():
    return render_template('05-form.html')

@app.route('/06-form',methods=['POST','GET'])
def formexe():
    # 接收04-form.html 传递过来的数据
    if request.method == 'GET':
        uname = request.args.get('uname','')
        upwd = request.args.get('upwd','')
        uemail = request.args.get('uemail','')
        ureal_name = request.args.get('ureal_name','')
        return render_template('06-form.html',params=locals())
    elif request.method == 'POST':
        uname = request.form.get('uname','')
        upwd = request.form.get('upwd','')
        uemail = request.form.get('uemail','')
        ureal_name = request.form.get('ureal_name','')
        print(uname,upwd,uemail,ureal_name)
        # 一定要ruturn一个字符串
        return '返回结果'

if __name__ == '__main__':
    # 运行Flask应用(启动Flask服务),默认会在本机开启5000端口,允许使用http://localhost:5000
    # 访问Flask的web应用
    # debug=True,将运行模式更改为调试模式(开发环境中推荐使用True,生产环境必须改为False)
    app.run(debug=True,port=5500)
    # 可在app.run中添加port参数,host参数 ,可修改端口号,默认为5000

