这只是一个测试用的代码，没有任何结构，所有代码服务端代码都在index.py当中，暂时不需要理解它。
服务端框架用的flask，它的模板渲染引擎是jinja2，所以跪求打算做前端的同学学习jinja2一下。
## 启动项目

python版本需要为python3
windows上应该不能运行，所以请在linux或macOS上运行

### 1. 依赖包安装

**安装依赖之前强烈建议用conda或venv创建一个新的python3环境。**

在项目根目录下执行命令`pip install -r requirements.txt`，等待安装完成。
### 2. 数据库
因为使用的是sqlite，所以不需要额外配置数据库。

### 3. 运行

项目根目录下执行命令`python index.py runserver`，然后在浏览器地址栏输入`localhost:5000`即可进入登录页面。使用账号`11111111`，密码`abc`即可登录名为狗蛋的个人资料页面。

## 用户创建

因为还没有实现管理员的功能，所以用户创建只能直接修改数据库。GitHub中的数据库里已经创建了一个用户狗蛋，账号为

在根目录下执行以下命令就可以创建一个账号为`22222222`，密码为`abc`，姓名为`二狗`，邮箱为`999@qq.com`的用户。

```python
python index.py shell     # 进入shell模式
>>> from index import db, User
>>> u = User(id='22222222', name='二狗', password='abc', email='999@qq.com')
>>> db.session.add(u)
>>> db.session.commit()
```

执行完上述命令后可以直接输入`quit()`退出，然后用`python index.py runserver`运行服务器，用浏览器实验是否已经添加该用户。也可以暂时不退出`shell`模式，继续输入:

```python
>>> User.query.all()
```

该命令执行后可以看到有两个用户，狗蛋和二狗。
