"""
管理应用的管理文件 
"""

'''
下列应用用于执行数据迁移以及在终端中执行数据库操作
'''
from flask_migrate import Migrate, MigrateCommand
# prompt_bool是用于删除数据库之前的提示,
from flask_script import Manager, Shell, prompt_bool
# 导入模型
from models import *
#主文件中导入app初始化manage
from config import app, db

#让python支持命令行工作
manager = Manager(app)
 
#使用migrate绑定app和db
migrate = Migrate(app,db)
 
#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)


#创建数据库
@manager.command
def create():
    db.create_all()
    return '数据库已创建'

#删除数据库
@manager.command
def drop():
    if prompt_bool('确定要删除数据库然后跑路吗？(确定请键入y)'):
        db.drop_all()
        return '数据库删除完成'
    return '删除需谨慎！'
 
if __name__ == '__main__':
    # 若没带命令,则会进入测试服务器环境
    manager.run()
