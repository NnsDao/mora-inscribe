import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()

# https://blog.csdn.net/weixin_44634704/article/details/106971379
# 装连接数据库的依赖项(django兼容mysqlclient,不兼容pymysql) 
# !!!装mysqlclient就不需要修改以下内容!!!
# 如果装pymysql的话得修改文件,在根路径下(这个django项目)文件下找到 __init__.py在里面写代码
