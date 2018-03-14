服务端框架采用的**flask**，有兴趣参与服务端开发的同学看参考书籍`Flask Web Development`。

**flask**框架模板渲染引擎是**jinja2**，所以有兴趣参与前端开发的同学学习一下**jinja2**。

[TOC]

## 目前已实现功能

* 用户登录、登出
* 所有用户的可公开资料可任意浏览，用户可以修改自己的资料
* 支持markdown的简单提问功能（回答功能尚未实现）



* 数据库迁移

## 项目配置

开发语言：python3

开发平台：Linux 或 macOS

注意：由于windows上某些依赖包无法安装，所以请在Linux或macOS上进行开发。

### 1. 依赖包安装

**安装依赖之前强烈建议用conda或virtualenv创建一个新的python3环境。**

**virtualenv**安装及使用教程：

```shell
# macOS或Linux安装命令
$ sudo easy_install virtualenv
# or
$ sudo pip install virtualenv
# Ubuntu可以使用
$ sudo apt-get install python-virtualenv

# virtual安装好后进入项目文件夹，在其下建立venv文件夹
$ cd project
$ virtualenv venv

# 当你要在项目中进行开发时，只需执行以下命令激活vene
$ . venv/bin/activate
```

安装依赖包：

在项目根目录下执行命令`pip install -r requirements.txt`，等待安装完成。

### 2. 数据库
因为使用的是**sqlite**，所以不需要额外配置数据库。

#### 数据库迁移

开发阶段如果对数据库模型进行了修改，可以通过以下命令更新数据库，同时不影响数据库中已存在的记录。

```python
python manage.py db migrate -m 'xxxxxxxx'
python manage.py db upgrade
```

其中'xxxxxxxx'为对本次更新的描述。

### 3. 运行

项目根目录下执行命令`python manage.py runserver`，然后在浏览器地址栏输入`localhost:5000`即可进入登录页面。

## 用户创建

GitHub中的数据库里已经创建了以下用户

| 账号     | 密码 | 用户名 |
| -------- | ---- | ------ |
| 11111111 | abc  | 狗蛋   |
| 22222222 | abc  | 二狗   |

### 1. 如何创建用户

因为还没有实现管理员的功能，所以用户创建只能直接修改数据库。

在根目录下执行以下命令就可以创建一个账号为`33333333`，密码为`abc`，姓名为`二哈`，邮箱为`999@qq.com`的用户。

```python
python manage.py shell     # 进入shell模式
>>> u = User(id='33333333', name='二哈', password='abc', email='999@qq.com')
>>> db.session.add(u)
>>> db.session.commit()
```

执行完上述命令后可以直接输入`quit()`退出，然后用`python manage.py runserver`运行服务器，用浏览器实验是否已经添加该用户。也可以暂时不退出`shell`模式，继续输入:

```python
>>> User.query.all()
```

该命令执行后可以看到有这些用户---狗蛋、二狗和二哈。

