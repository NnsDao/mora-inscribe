# ic_principal
```sh
ic 数据获取,最顶级可以创建用户的星球 

# 顶级canister https://dashboard.internetcomputer.org/canister/53i5d-faaaa-aaaan-qda6a-cai


```
# 安装依赖
```sh
pip install -r requirements.txt


```

# 使用
```sh
# 根据顶级canister获取所有 子canister,再获取每个 子canister 的所有文章,进行统计
python ic_query_user_articles.py

# 根据文章id获取文章的详细信息
python ic_query_article.py


```



# 参考 https://github.com/rocklabs-io/ic-py

