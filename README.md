## 启动项目

python版本需要为python3

### 1. 依赖包安装

**安装依赖之前强烈建议用conda或venv创建一个新的python3环境。**

在项目根目录下执行命令`pip install -r requirements.txt`，等待安装完成。

### 2. 运行

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