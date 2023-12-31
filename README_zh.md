# ic_principal
```sh
ic 数据获取,最顶级可以创建用户的星球 

# 顶级canister  queryCanisterIds
# https://dashboard.internetcomputer.org/canister/53i5d-faaaa-aaaan-qda6a-cai


```
# 安装依赖
```sh
pip install -r requirements.txt


```

# 使用
```sh
# 根据顶级canister获取所有 子canister,再获取每个 子canister 的所有文章,进行统计
python manage.py ic_query_user_article_list

# 根据文章id获取文章的详细信息
python manage.py ic_query_article


```



# 参考 https://github.com/rocklabs-io/ic-py

```sh
# django安装教程
pip install -i https://pypi.douban.com/simple Django
# 查看版本
django-admin version
python3 -m django --version
# 创建一个项目
django-admin startproject mysite
mysite/                 # 项目的容器
├── manage.py           # 管理文件，可让你以各种方式与该 Django 项目进行交互
└── mysite              # 项目目录
    ├── __init__.py     # 一个空文件，告诉 Python 该目录是一个 Python 包
    ├── settings.py     # 配置文件
    ├── asgi.py         # asgi服务器来处理websocket请求
    ├── urls.py         # 路由系统 --> URL和函数的对应关系
    └── wsgi.py         # runserver命令就使用wsgiref模块做简单的web server
# 创建app应用
python manage.py startapp ic_app  [app名（通常为appXX，如：app01）]
mysite/                                 # 项目的容器
├── manage.py                           # 管理文件，可让你以各种方式与该 Django 项目进行交互
└── mysite                              # 项目目录
    ├── __init__.py                     # 一个空文件，告诉 Python 该目录是一个 Python 包
    ├── settings.py                     # 配置文件
    ├── asgi.py                         # asgi服务器来处理websocket请求
    ├── urls.py                         # 路由系统 --> URL和函数的对应关系
    └── wsgi.py                         # runserver命令就使用wsgiref模块做简单的web server
└──ic_app                               # app应用
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    └── ic_controller                   # 业务代码
        ├── __init__.py
        ├── ic_query_user_articles.py   #
        └── ic_query_article.py         # 
    └── management                      # 自定义命令
        ├── __init__.py
        └── commands
            ├── __init__.py
            ├── my_script.py            # python manage.py my_script arg1 arg2
            └── my_script_two.py
    └── migrations                      # 迁移文件
        ├── __init__.py
        └── __init__.py
    ├── models.py                       # 数据库表
    ├── tests.py
    ├── urls.py
    └── views.py
└──db.sqlite3                           # sqlite3 数据库


# django数据库 字段
# https://www.cnblogs.com/yuanxiaojiang/p/17181278.html
# https://www.cnblogs.com/dengz/p/11462441.html
# https://zhuanlan.zhihu.com/p/653890253?utm_id=0
# 数据库 迁移  db.sqlite3
python manage.py makemigrations
python manage.py migrate
# Django只为更改的部分生产迁移文件

# python django 操作数据库查询 
# https://blog.csdn.net/a6864657/article/details/97694195
# https://docs.djangoproject.com/en/3.2/topics/db/queries/
# https://blog.csdn.net/weixin_50804299/article/details/131409177
# https://blog.51cto.com/u_12205/6701791
# https://www.liujiangblog.com/course/django/129
# 数据库分页
# https://zhuanlan.zhihu.com/p/646760631
# https://docs.djangoproject.com/zh-hans/3.2/topics/pagination/
# https://zhuanlan.zhihu.com/p/619625858
# https://www.zhuxianfei.com/python/44314.html
# https://blog.csdn.net/qq_37605109/article/details/124514037





# 数据库分页 前后分离 API返回数据
# https://codeleading.com/article/19525198135/
# https://www.cnblogs.com/diaozhabing/p/10871194.html

# 启动django项目
python manage.py runserver
# 访问
# http://127.0.0.1:8000/get_op_tick_list?page=2&size=12
# http://127.0.0.1:8000/get_op_tick_list?page=2&size=2&op_tick_group_key=deploy_wow
# http://127.0.0.1:8000/get_article_list?page=2&size=5&atype=Article&article_id=0D5VQRQK0AH9VY7Q1EPXSRM3RR
# http://api.icpscriptions.com/get_article_list


# linux 部署
ls -laih uwsgi_config




# 问题
# https://www.coder.work/article/6702501
# https://www.coder.work/article/4946996
# https://blog.csdn.net/qq_42701659/article/details/130740889
# https://www.coder.work/article/2407032
# https://www.jianshu.com/p/2fd01e7ee247
# https://blog.csdn.net/SDKL_YI/article/details/129088153

# 后台进程  nohup ./ic_query_user_article_list.sh > ic_query_user_article_list.log 2>&1  &
# https://zhuanlan.zhihu.com/p/617627144?utm_id=0
# https://blog.csdn.net/Dontla/article/details/126343988
# https://blog.csdn.net/qq_21891743/article/details/132769245

cd /www/wwwroot/api.icpscriptions.com
# 后台运行
nohup bash ic_query_user_article_list.sh > ic_query_user_article_list.log 2>&1 &
# nohup bash echo_test.sh > ic_query_user_article_list.log 2>&1 &
ps -aux | grep 'ic_query_user_article_list'
tail -f ic_query_user_article_list.log
jobs
# 后台程序正确的退出 [1]+  Done                    bash ic_query_user_article_list.sh > ic_query_user_article_list.log 2>&1

# /usr/local/lib/python3.9/site-packages/ic/client.py
# def query(self



# 程序出现 killed
# https://zhuanlan.zhihu.com/p/648165521?utm_id=0

```