# README

## Motivation
A course project for course management system.

Course: System Analysis and Design

School of Data and Computer Science, Sun Yat-Sen University

## 目前已实现功能

* 用户登录、登出
* 所有用户的可公开资料可任意浏览，用户可以修改自己的资料
* 支持markdown的简单提问功能（回答功能尚未实现）
* 创建课程、查看课程列表
* 发布作业，查看作业，下载作业文件


* 数据库迁移

## 部分功能说明

### 创建课程

* 创建课程时，用户可以提供学生名单(暂时只支持csv)，该csv文件至少要提供两个字段*id*，*name*，分别为学生的学号与姓名。系统判断学生是否为已注册用户，若不是则创建该用户，初始密码为*学号*。

## 文件结构

```
|-Course/
    |-app/                          # 程序包
        |-api/                      # api蓝图
        |-main/                     # 主页登录登出相关蓝图
        |-profile/                  # 个人资料相关蓝图
        |-course/                   # 课程相关蓝图
        |-error/                    # 错误处理相关蓝图
        |-static/                   # 图片及css等静态文件
        |-template/                 # html模版
        |-__init__.py               # 程序工厂函数
        |-models.py                 # 数据库模型
        |-util.py                   # 辅助函数包
    |-doc/                          # 文档
        |-Request Analysis.docx     # 需求分析文档
    |-test/							# 测试工具
        |student_list.py			# 随机生成学生名单
    |-migrations/                   # 数据库迁移脚本
    |-Dockerfile                    # Docker
    |-README.md                     # README
    |-config.py                     # 程序配置文件
    |-data-dev.sqlite               # sqlite数据库
    |-manage.py                     # 启动程序
    |-requirements.txt              # 依赖包需求文件
```

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

## 测试

### 学生名单生成

为了方便开发时测试，在test文件夹里的student_list.py提供了随机生成学生名单的功能。