from django.db import models

# Create your models here.


 

# class Person(models.Model):
#     name = models.CharField(max_length=30)
#     age = models.IntegerField()


# class op_deploy_tick(models.Model):
#     name = models.CharField(max_length=30)
#     age = models.IntegerField()
#     # # 总供应
#     # "max_supply":0,
#     # # 持有人数-去重author
#     # "holders":0,
#     # # 如果当前文章abstract的值是deploy 就取当前文章的created字段
#     # "create":"",
#     # # 进度 当前mint的数量/总供应 [每一张铭文{文章}的amt是1000 当第21个被mint那进度就是100%]
#     # "progress":"",
#     # # 分组固定值
#     # "tick":"icps",
#     # # 当前文章 abstract 下的 amt 值
#     # "amt":"",
#     # # 当前文章 abstract 下的 op 值
#     # "op":"deploy",
#     # # 当前文章 abstract 下的 p值
#     # "protocol":"",

class op_tick_group(models.Model):
    # # 自定义自增列
    # nid = models.AutoField(primary_key=True)

    # 自动创建一个列名为id的且为自增的整数列
    article_id = models.CharField(max_length=40)
    op_tick_group_key = models.CharField(max_length=30)
    title = models.CharField(max_length=90)
    # import datetime
    # created = 1609459200000  # 示例毫秒时间
    # 1609459200123
    # dt = datetime.datetime.fromtimestamp(created / 1000.0)    
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    # - 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807

    author = models.CharField(max_length=90)
    canister_id = models.CharField(max_length=90)
    protocol = models.CharField(max_length=90)
    op = models.CharField(max_length=90)
    tick = models.CharField(max_length=90)
    tags = models.CharField(max_length=90)


    amt = models.IntegerField()
    max = models.BigIntegerField()
    lim = models.IntegerField()
    # https://tool.lu/timestamp
    # 2147483647
    # 2147483647

    create_time = models.DateTimeField(auto_now_add=True)  # 入库创建时间 
    update_time = models.DateTimeField(auto_now=True)      # 入库更新时间
    
 
    # "article_id":article_id,
    # "op_tick_group_key":op_tick_group_key,

    # "title":items_line["title"],
    # "created":items_line["created"],
    # "updated":items_line["updated"],

    # "page":items_line["page"],
    # "tags":items_line["tags"],

    # "author":items_line["author"],
    # "canister_id":items_line['user_canister_id'],
    # "canister_index":items_line["canister_index"],
    
    # "protocol":abstract_json["p"],
    # "op":abstract_json["op"],
    # "tick":abstract_json["tick"],
    # "amt":abstract_json["amt"] if 'amt' in abstract_json else '',
    # "max":abstract_json["max"] if 'max' in abstract_json else '',
    # "lim":abstract_json["lim"] if 'lim' in abstract_json else '',

    '''
    {
        'id': '0C9YCESX6J5TV183NEX5G1DPCJ', 'status': {'Public': None}, 'thumb': 'QmeVYdJ4jvV6GcHbE7DdMaNowU2WsnNTibGRkw4oswnWui', 
        'title': 'FKDOM', 'created': 1702386004349, 
        'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 'cate': 0, 'like': 0, 'tags': [], 
        'view': 0, 'fromurl': '', 'unlike': 0, 
        'author': 'ycaq2-am5es-7ddcs-u5keb-5xawp-k4d3w-tsilc-hd2fk-tiuy4-wopfn-jae', 'commentTotal': 0, 'comment': 0, 
        'updated': 1702386028053, 
        'abstract': 'Deploy: { "p": "mora-20", "op": "deploy", "tick": "fkdom", "max": "2100", "lim": "1" } ', 'allowComment': False, 
        'copyright': [], 'original': True, 
        'commentNew': 0, 'user_canister_id': 'tcaj5-pyaaa-aaaan-qdb4q-cai', 'canister_index': 4, 'page': 1, 'op_tick_group_key': 'deploy_fkdom', 
        'abstract_json': {'p': 'mora-20', 'op': 'deploy', 'tick': 'fkdom', 'max': '2100', 'lim': '1'}
    }
    '''

class article_list(models.Model):

    # 自动创建一个列名为id的且为自增的整数列
    article_id = models.CharField(max_length=40)
    article_status = models.CharField(max_length=30)
    thumb = models.CharField(max_length=130)
    # article_thumb = models.CharField(max_length=130)
    title = models.CharField(max_length=90)
    # import datetime
    # created = 1609459200000  # 示例毫秒时间
    # 1609459200123
    # dt = datetime.datetime.fromtimestamp(created / 1000.0)    
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    # - 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807

    toped = models.IntegerField()
    subcate = models.IntegerField()
    atype = models.CharField(max_length=30)
    cate = models.IntegerField()
    like = models.BigIntegerField()
    tags = models.CharField(max_length=90)
    view = models.BigIntegerField()
    fromurl = models.CharField(max_length=190)
    unlike = models.BigIntegerField()
    comment_total = models.BigIntegerField()
    comment = models.BigIntegerField()
    allow_comment = models.BooleanField(verbose_name='是否:0 false,1true',default=False)
    copyright = models.CharField(max_length=90)
    original = models.BooleanField(verbose_name='是否:0 false,1true',default=False)
    comment_new = models.BigIntegerField()
    

    author = models.CharField(max_length=90)
    canister_id = models.CharField(max_length=90)
    protocol = models.CharField(max_length=90)
    op = models.CharField(max_length=90)
    tick = models.CharField(max_length=90)

    abstract = models.TextField()

    amt = models.IntegerField()
    max = models.BigIntegerField()
    lim = models.IntegerField()
    # https://tool.lu/timestamp

    create_time = models.DateTimeField(auto_now_add=True)  # 入库创建时间 
    update_time = models.DateTimeField(auto_now=True)      # 入库更新时间
    
 








