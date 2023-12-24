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


# 部署

```sh
# 数据库配置
cp .env.example .env

# 查看版本
django-admin version
python3 -m django --version

# 数据库 迁移  db.sqlite3
python manage.py makemigrations
python manage.py migrate
# Django只为更改的部分生产迁移文件


# 本地启动django项目
python manage.py runserver
# 访问
# http://127.0.0.1:8000/get_op_tick_list?page=2&size=12
# http://127.0.0.1:8000/get_op_tick_list?page=2&size=2&op_tick_group_key=deploy_wow
# http://127.0.0.1:8000/get_article_list?page=2&size=5&atype=Article&article_id=0D5VQRQK0AH9VY7Q1EPXSRM3RR



# linux 部署
ls -la uwsgi_config

```





# 参考 https://github.com/rocklabs-io/ic-py


