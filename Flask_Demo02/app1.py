from flask import Flask,url_for,render_template

# 将当前运行的主程序构建成Flask应用,以便接收用户的请求(request)和响应(response)
app = Flask(__name__)


@app.route('/01-var')
def var_views():
    name = '隔壁老王'
    age = 32
    salary = 125.55
    tup=('老魏','老王','老吕','小蒙蒙')
    list = ['漩涡鸣人','宇智波佐助','春野樱']
    dic = {
        'C':'CHINA',
        'A':'AMERICA',
        'J':'JAPAN',
    }
    dog = Dog()
    return render_template('01-var.html',params=locals())

# 此示例展示过滤器的作用
@app.route('/02-filter')
def filter_views(uname):
    title = ' this is my FIRST filter page'
    return render_template('02-filter.html',title=title)


# 此示例if标签的用法
@app.route('/03-if/<uname>')
@app.route('/03-if')
def if_views(uname=None):
    return render_template('03-if.html',age=35,name=uname)

# 此示例示意for结构的用法
@app.route('/04-for')
def for_views():
    list = ['武大郎','潘金莲','王宝强','王伟超']
    dic={
        'SWK':'孙悟空',
        'ZBJ':'猪八戒',
        'SWJ':'孙悟空',
        'WWC':'王伟超',
        'TSZ':'唐三藏',
    }
    print(f'dic.values():{dic.items()}')
    # dic.keys():dict_keys(['SWK', 'ZBJ', 'SWJ', 'WWC', 'TSZ'])
    # dic.values():dict_values(['孙悟空', '猪八戒', '孙悟空', '王伟超', '唐三藏'])
    # dic.items():dict_items([('SWK', '孙悟空'), ('ZBJ', '猪八戒'), ('SWJ', '孙悟空'), ('WWC', '王伟超'), ('TSZ', '唐三藏')])
    return render_template('04-for.html',params=locals())


# 此示例示意宏的用法
@app.route('/05-macro')
def macro_views():
    list = ['武大郎','潘金莲','王宝强','王伟超']

    return render_template('05-macro.html',params=locals())

@app.route('/06-static')
def static_views():
    list = ['武大郎','潘金莲','王宝强','王伟超']
    return render_template('06-static.html',params=locals())

class Dog(object):
    name = '旺财'
    def eat(self):
        return self.name + '吃狗粮'
    



if __name__ == '__main__':
    # 运行Flask应用(启动Flask服务),默认会在本机开启5000端口,允许使用http://localhost:5000
    # 访问Flask的web应用
    # debug=True,将运行模式更改为调试模式(开发环境中推荐使用True,生产环境必须改为False)
    app.run(debug=True,port=5500)
    # 可在app.run中添加port参数,host参数 ,可修改端口号,默认为5000

