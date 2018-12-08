from flask import Flask,render_template,request,redirect,make_response

# 将当前运行的主程序构建成Flask应用,以便接收用户的请求(request)和响应(response)
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/list')
def listindex():
    return render_template('list.html')


@app.route('/login')
def login():
    return render_template('login.html')


# 请求方式为post,一定要注明methods=['GET','POST']
@app.route('/form',methods=['GET','POST'])
def form():
    if request.method == 'GET':
        username = request.args.get('username','')
        password = request.args.get('password','')
        # 如果用户名是admin并且密码也是admin,去/路径
        if username == 'admin' and password == 'admin':
            # 登陆成功,重定向到'/'
            return redirect('/')
        else:
            # 使用响应对象输出'用户名或密码不正确'
            resp = make_response('用户名或者密码不正确')
            return resp


    elif request.method == 'POST':
        # 接收前端请求提交的数据
        username = request.form.get('username','')
        password = request.form.get('password','')
        return f"username:{username},password:{password}"





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500



if __name__ == '__main__':
    # 运行Flask应用(启动Flask服务),默认会在本机开启5000端口,允许使用http://localhost:5000
    # 访问Flask的web应用
    # debug=True,将运行模式更改为调试模式(开发环境中推荐使用True,生产环境必须改为False)
    app.run(debug=True,port=5000)
    # 可在app.run中添加port参数,host参数 ,可修改端口号,默认为5000

