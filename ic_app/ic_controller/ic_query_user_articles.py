#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
from ic.canister import Canister
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import Types
from ic import Principal
# 线程池
from concurrent.futures import ThreadPoolExecutor,as_completed
import time
import datetime
import math
import json
import os
import shutil
from config import get_root

# from ic_app.xhsParser import xhsHtmlInfoObj
# RuntimeError: Model class models.studentsInfo doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
# https://blog.csdn.net/ywk_hax/article/details/83421174
# 解决方法,在导入models的时候,最好加上app应用名
from ic_app.models import op_tick_group as OpTickGroupModel,article_list as ArticleListModel

# 最顶级可以创建用户的星球
# https://dashboard.internetcomputer.org/canister/53i5d-faaaa-aaaan-qda6a-cai
# https://github.com/rocklabs-io/ic-py




class ic_data_statistics():
    def __init__(self) -> None:
        # 类似于Linux的用户
        self.root_canister_id = '53i5d-faaaa-aaaan-qda6a-cai'
        self.user_init_canister_id = 'rrkah-fqaaa-aaaaa-aaaaq-cai'
        self.my_canister_id = 'gkhdz-7yaaa-aaaan-qi2ra-cai'
        # efi2f-baaaa-aaaan-qja5a-cai
        iden = Identity()
        self.client = Client()
        self.agent = Agent(iden, self.client)
        self.get_root_path = get_root()
        # 去重.
        self.file_is_exists = os.path.join(self.get_root_path, 'file_is_exists')
        self.op_tick_group_is_exists_key = os.path.join(self.file_is_exists, 'op_tick_group_key')
        # 同一个用户下的文章ID是否存在文件
        self.canister_id_article_id_is_exists_path = os.path.join(self.file_is_exists, 'canister_id_article_id')
        root_inittrail_path = os.path.join(self.get_root_path, 'root_inittrail.did')
        user_plant_path = os.path.join(self.get_root_path, 'user_plant.did')
        self.root_governance_did = open(root_inittrail_path, "r", encoding="utf-8").read()
        self.user_governance_did = open(user_plant_path, "r", encoding="utf-8").read()
        self.governance = Canister(agent=self.agent, canister_id=self.root_canister_id, candid=self.root_governance_did)
        time_current = getTime()
        # formatted_total_start_time = time_current['formatted_time']
        forma_ted_time = time_current['forma_ted_time']
        
        self.json_root_path = os.path.join(self.get_root_path, 'json_data_path')
        self.json_data_path = os.path.join(self.get_root_path, self.json_root_path ,forma_ted_time)
        # 删除目录
        remove_folder(self.json_root_path)
        # 创建目录
        mk_dir(self.json_data_path)
        # 删除目录
        remove_folder(self.op_tick_group_is_exists_key)
        # 创建目录
        mk_dir(self.op_tick_group_is_exists_key)
        # 删除目录
        remove_folder(self.canister_id_article_id_is_exists_path)
        # 创建目录
        mk_dir(self.canister_id_article_id_is_exists_path)
        ''' 
        {
            'id': '0C20JGKA95ZCYP88F4T6D1DH40', 
            'status': {'Public': None}, 'thumb': 'QmWaxEVLUfG3fdpnyEmFxaNqxn9kxWZeayEJ4RUGpFnbfn', 'title': 'ICPS', 'created': 1702113370041, 'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 
            'cate': 0, 'like': 0, 'tags': [], 'view': 0, 'fromurl': '', 'unlike': 0, 'author': Principal(b6lk6-zdgf2-dzhpr-5guxn-rajnt-t5cze-tkmtd-jb5xg-hnweg-wcwqs-3qe), 
            'commentTotal': 0, 'comment': 0, 'updated': 1702113370041, 
            'abstract': 'Mint: { "p": "icps-20", "op": "mint", "tick": "icps", "amt": "1000" }', 
            'allowComment': False, 'copyright': [], 'original': True, 'commentNew': 0
        }
        '''
        # 所有的数据列表
        self.all_data_list_path = os.path.join(self.json_data_path, 'all_data_list_path.jsonl')
        # 分批次保存到数据库 所有的数据
        self.batch_save_data_list = []
        # 总的数据统计
        # self.total_data_dict_path = os.path.join(self.json_data_path, 'total_data_dict_path.json')
        # op是deploy的根据tick分组统计
        self.op_deploy_tick_group_data_list_path = os.path.join(self.json_data_path, 'op_deploy_tick_group_data_list_path.jsonl')
        self.op_deploy_tick_group_data_dict = {
            # "icps":{
            #     # 总供应
            #     "max_supply":0,
            #     # 持有人数-去重author
            #     "holders":0,
            #     # 如果当前文章abstract的值是deploy 就取当前文章的created字段
            #     "create":"",
            #     # 进度 当前mint的数量/总供应 [每一张铭文{文章}的amt是1000 当第21个被mint那进度就是100%]
            #     "progress":"",
            #     # 分组固定值
            #     "tick":"icps",
            #     # 当前文章 abstract 下的 amt 值
            #     "amt":"",
            #     # 当前文章 abstract 下的 op 值
            #     "op":"deploy",
            #     # 当前文章 abstract 下的 p值
            #     "protocol":"",
            # },
        }

        # 根据op以及tick分组去重[文章id]的列表 [目前外部op有deploy,Mint]
        self.op_tick_group_data_list_path = os.path.join(self.json_data_path, 'op_tick_group_data_list_path.jsonl')
        self.op_tick_group_data_dict = {
            # "mint_icps":[]
        }
        self.op_tick_article_id_key_dict = {}

        self.indes_canister_data_dict_path = os.path.join(self.json_data_path, 'indes_canister_data_dict_path_log.jsonl')

    def get_type_name(self,obj):
        ''' 获取类型的名称 '''
        return type(obj).__name__
    def query_canister_ids(self):
        ''' 快照的形式一次性返回全部不重复的id '''
        res = self.governance.queryCanisterIds()
        data_list = res[0]
        ret_all = []
        print(  len(data_list),self.get_type_name(data_list)  )
        for index, value in enumerate(data_list):
            # if index >= 15:
            #     continue
            time_start_current = getTime()
            formatted_start_time = time_start_current['formatted_time']
            # forma_ted_total_start_time = time_start_current['forma_ted_time']
            # print('')
            # print('Index: {}, Value: {}'.format(index, value))
            del data_list[index]
            ret = self.thread_pool_articles(user_canister_id=value,canister_index=index)
            time_end_current = getTime()
            formatted_end_time = time_end_current['formatted_time']
            # print('formatted_start_time=',formatted_start_time,'formatted_end_time=',formatted_end_time,len(ret)  )
            # ret_all.append(ret)
        # 保存   op以及tick分组去重 
        # self.save_config_json(config_path=self.op_tick_group_data_list_path,config_dict_data=self.op_tick_group_data_dict)
        return ret_all
    def thread_pool_data(self,max_worker=600):
        '''
        线程池
        '''
        res = self.governance.queryCanisterIds()
        data_list = res[0]
        # data_list = res[0][0:10]
        # data_list = res[0][0:1000]
        # print('--max_worker--',max_worker)
        with ThreadPoolExecutor(max_workers=max_worker) as t:
            obj_list = []
            for index, canister_id in enumerate(data_list):
                # if index >= 1000:
                #     continue
                # print('')
                # msg = 'Index: {}, canister_id: {}'.format(index, canister_id)
                # print(msg)
                # item_line = {
                #     "msg":msg
                # }
                # append_to_jsonl(file_path=self.indes_canister_data_dict_path, data=item_line)
                del data_list[index]
                obj = t.submit(self.thread_pool_articles, canister_id,index)
                # obj_list.append(obj)
            '''
            # 如果你需要等待所有任务完成，可以使用以下代码
            for future in as_completed(obj_list):
                ret_canister_articles_data = future.result()
                if not ret_canister_articles_data:
                    # print('')
                    # print('')
                    print('--空的数据-',ret_canister_articles_data)
                    # print('')
                    continue
                # article_num = 0
                # article_total = len(ret_canister_articles_data)
                # print('')
                # print('')
                # print('')
                # 记录每个文章
                # self.make_canister_article_list(ret_canister_articles_data)
                # print("返回的",ret_canister_articles_data)
                # print(f"返回的描述: {data['desc']}")
                # print('')
                # print('')
                # print('--article_total--',article_total)
                # print('')
            '''

        # 保存   op以及tick分组去重 
        # self.save_config_json(config_path=self.op_tick_group_data_list_path,config_dict_data=self.op_tick_group_data_dict)
        # 删除目录
        remove_folder(self.op_tick_group_is_exists_key)
        # 删除目录
        remove_folder(self.canister_id_article_id_is_exists_path)
        # self.make_op_tick_list()
    def make_op_tick_list(self):
        article_total = len(self.op_tick_group_data_dict)
        index = 0
        multi_data_list = []
        batch_num = 200
        multi_total = 0
        for key ,item in self.op_tick_group_data_dict.items():
            index += 1

            multi_data_list.append(item)
            if index % batch_num == 0 or index == article_total:
                # multi_total += len(multi_data_list)
                multi_len = len(multi_data_list)
                multi_total += multi_len
                # print('----item--',self.get_type_name(item),'--article_total--',article_total ,'-index-',index,'-multi_total-',multi_total,'-multi_len-',multi_len)
                self.multi_save_op_tick_list_to_db(multi_data_list)
                multi_data_list = []
    def make_op_tick_bak_list(self):
        '''  '''
        for key ,op_tick_group_list in self.op_tick_group_data_dict.items():
        # for key ,op_tick_group_list in self.op_tick_group_data_dict:
            # print('')
            # print('--key ,value--',key ,op_tick_group_list)
            # 总文章数
            article_total = len(op_tick_group_list)
            # print(  article_total,self.get_type_name(canister_articles_list)  )
            # print('')
            multi_data_list = []
            multi_total = 0
            # 一次处理多少个文章
            batch_num = 200
            for index, item in enumerate(op_tick_group_list):
                # print('')
                # item: dict
                index += 1
                # print('----item--',self.get_type_name(item),'--article_total--',article_total ,'-index-',index)
                # print('----item--',item)
                '''
                ----item-- {'id': '0C04SGYAMVYNNYZYWF81GV5V8F', 'status': {'Public': None}, 'thumb': 'QmVtDL4UyJjHUae8b6vESaimb59kebprkagMmawE2HSUiq', 'title': 'MORA ', 'created': 1702049161438, 'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 'cate': 0, 'like': 0, 'tags': [], 'view': 0, 'fromurl': '', 'unlike': 0, 'author': 'e2yd5-tlpth-eejos-g6v5h-irhiw-urz74-qdvdx-skpmm-7o3c3-jcbrn-iae', 'commentTotal': 0, 'comment': 0, 'updated': 1702049456326, 'abstract': 'Mint: { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" } tag：$mora \n', 'allowComment': False, 'copyright': [], 'original': True, 'commentNew': 0, 'user_canister_id': 't6etm-yyaaa-aaaan-qdb6q-cai', 'canister_index': 8, 'page': 5, 'op_tick_group_key': 'mint_mora', 'abstract_json': {'p': 'mora-20', 'op': 'mint', 'tick': 'mora', 'amt': '1000'}}
                '''

                multi_data_list.append(item)
                if index % batch_num == 0 or index == article_total:
                    # multi_total += len(multi_data_list)
                    multi_len = len(multi_data_list)
                    multi_total += multi_len
                    # print('----item--',self.get_type_name(item),'--article_total--',article_total ,'-index-',index,'-multi_total-',multi_total,'-multi_len-',multi_len)
                    self.multi_save_op_tick_list_to_db(multi_data_list)
                    multi_data_list = []
    def multi_save_op_tick_list_to_db(self,multi_data_list:list=[]):
        ''' '''
        # --key ,value-- deploy_tuo [{'article_id': '0D5VQRQK0AH9VY7Q1EPXSRM3RR', 'op_tick_group_key': 'deploy_tuo', 'title': 'tuo', 'created': 1703345128003, 'updated': 1703345128003, 'page': 1, 'tags': [], 'author': 'ycaq2-am5es-7ddcs-u5keb-5xawp-k4d3w-tsilc-hd2fk-tiuy4-wopfn-jae', 'canister_id': 'tcaj5-pyaaa-aaaan-qdb4q-cai', 'canister_index': 4, 'protocol': 'mora-20', 'op': 'deploy', 'tick': 'tuo', 'amt': '', 'max': '21000', 'lim': '1'}]
        if not multi_data_list:
            return ''
        article_id_list = [ i['id'] for i in multi_data_list ]
        # order_by("-created").
        article_list_model = OpTickGroupModel.objects.filter(article_id__in=article_id_list).values(
                # 'id', 
                'article_id'
                # ,'created','op_tick_group_key'
                # ,'article_status','thumb',
                # 'title','updated','toped','subcate','atype','cate','like','tags','view',
                # 'fromurl','unlike','comment_total','comment','allow_comment','copyright','original',
                # 'comment_new','author','canister_id','protocol','op','tick','abstract','amt','max','lim',
                # 'create_time','update_time'
        )
        article_id_list = []
        # datetime.datetime(2023, 12, 23, 15, 45, 28, 715241, tzinfo=datetime.timezone.utc)}
        # print('')
        # count = article_list_model.count()
        # print('--article_list_model--',article_list_model,self.get_type_name(article_list_model),'-count-',count )
        # --article_list_model-- <QuerySet [<article_list: article_list object (4)>]> QuerySet -count- 1
        # --article_list_model-- <QuerySet [{'id': 1, 'article_id': '0C06JCQHBT5NXWCHPDKG7C18C9'}, {'id': 2, 'article_id': '0C06EDN154324KZER2JTHM9P0A'}]> QuerySet -count- 2
        # --article_list_model-- <QuerySet []> QuerySet
        article_exist_id_list = [ t['article_id'] for t in article_list_model]
        article_list_model = []


        # install_article_data = []
        obj_install_data = []
        for index, row in enumerate(multi_data_list):
            # print('')
            article_id = row['id']
            if article_id not in article_exist_id_list:
                # 将数据转换为JSON格式
                tags = row.get('tags'),
                json_tags = ''
                if tags:
                    json_tags = json.dumps(tags,ensure_ascii=False)

                data = OpTickGroupModel(
                    article_id = row.get('id'),
                    op_tick_group_key = row.get('op_tick_group_key'),

                    # thumb = row.get('thumb'),
                    title =  row.get('title'),
                    # import datetime
                    # created = 1609459200000  # 示例毫秒时间
                    # 1609459200123
                    # dt = datetime.datetime.fromtimestamp(created / 1000.0)    
                    created =  row.get('created'),
                    updated =  row.get('updated'),
                    # - 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807
                    # django.db.utils.IntegrityError: NOT NULL constraint failed: ic_app_op_tick_group.canister_id


                    tags =  json_tags,
                    # view = row.get('view'),
                    # fromurl = row.get('fromurl'),
                    # unlike = row.get('unlike'),
                    # comment_total = row.get('commentTotal'),
                    # comment = row.get('comment'),
                    # allow_comment = row.get('allowComment'),
                    # copyright = json_copyright,
                    # original = row.get('original'),
                    # comment_new = row.get('commentNew'),

                    author = row.get('author'),
                    canister_id = row.get('user_canister_id'),

                    # {'p': 'mora-20', 'op': 'mint', 'tick': 'mora', 'amt': '1000'}
                    protocol = row.get('protocol'),
                    op = row.get('op'),
                    tick = row.get('tick'),

                    amt = row.get('amt') if 'amt' in row else 0,
                    max = row.get('max') if 'max' in row else 0,
                    lim = row.get('lim') if 'lim' in row else 0,

                    # create_time = create_time,      # 入库创建时间 
                    # update_time = create_time,      # 入库更新时间

                )
                obj_install_data.append(data)
                # install_article_data.append(row)
            # print('--article--item--',item)
            del multi_data_list[index]
        # print('--install_article_data--',len(install_article_data) ,self.get_type_name(install_article_data) )

        # # https://tool.lu/timestamp
        # # 2147483647
        # # 2147483647
        # TypeError: op_tick_group() got unexpected keyword arguments: 'original', 'comment_new'


        if obj_install_data:
            OpTickGroupModel.objects.bulk_create(obj_install_data)
        article_exist_id_list = []
        obj_install_data = []
        # 
    def make_canister_article_list(self,canister_articles_list=[]):
        ''' 处理线程池返回的 canister 文章数据'''
        article_num = 0
        # print('')
        # print('')
        # print('')
        # 总文章数
        article_total = len(canister_articles_list)
        # print(  article_total,self.get_type_name(canister_articles_list)  )
        # print('')
        multi_data_list = []
        multi_total = 0
        # 一次处理多少个文章
        batch_num = 200
        for index, item in enumerate(canister_articles_list):
            # print('')
            # item: dict
            index += 1
            # print('----item--',self.get_type_name(item),'--article_total--',article_total ,'-index-',index)
            # print('----item--',item)
            '''
            ----item-- {'id': '0C04SGYAMVYNNYZYWF81GV5V8F', 'status': {'Public': None}, 'thumb': 'QmVtDL4UyJjHUae8b6vESaimb59kebprkagMmawE2HSUiq', 'title': 'MORA ', 'created': 1702049161438, 'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 'cate': 0, 'like': 0, 'tags': [], 'view': 0, 'fromurl': '', 'unlike': 0, 'author': 'e2yd5-tlpth-eejos-g6v5h-irhiw-urz74-qdvdx-skpmm-7o3c3-jcbrn-iae', 'commentTotal': 0, 'comment': 0, 'updated': 1702049456326, 'abstract': 'Mint: { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" } tag：$mora \n', 'allowComment': False, 'copyright': [], 'original': True, 'commentNew': 0, 'user_canister_id': 't6etm-yyaaa-aaaan-qdb6q-cai', 'canister_index': 8, 'page': 5, 'op_tick_group_key': 'mint_mora', 'abstract_json': {'p': 'mora-20', 'op': 'mint', 'tick': 'mora', 'amt': '1000'}}
            '''

            multi_data_list.append(item)
            if index % batch_num == 0 or index == article_total:
                # multi_total += len(multi_data_list)
                multi_len = len(multi_data_list)
                multi_total += multi_len
                # print('----item--',self.get_type_name(item),'--article_total--',article_total ,'-index-',index,'-multi_total-',multi_total,'-multi_len-',multi_len)
                # self.multi_save_article_list_to_db(multi_data_list)
                multi_data_list = []


        # print('')
        # print('')
    def multi_save_article_list_to_db(self,multi_data:list = []):
        ''' 批量保存文章信息 '''
        if not multi_data:
            return ''
        article_id_list = [ i['id'] for i in multi_data ]
        # print('--article_id_list--',article_id_list,'--len--',len(article_id_list) ,'')
        # in：是否包含在范围内 查询编号为1或3或5 book = Book.objects.filter(id__in=[1, 3, 5])
        # 查询学过课程id为1和2的所有同学的id、姓名
        # Student.object.filter(scorecoursein=[1, 2]).values('id', 'name').distinct()
        # article_list_model = ArticleListModel.objects.filter(article_id__in=article_id_list).all()
        # article_id = row.get('id'),
        # order_by("-created").
        article_list_model = ArticleListModel.objects.filter(article_id__in=article_id_list).values(
                # 'id', 
                'article_id'
                # ,'created','article_status','thumb',
                # 'title','updated','toped','subcate','atype','cate','like','tags','view',
                # 'fromurl','unlike','comment_total','comment','allow_comment','copyright','original',
                # 'comment_new','author','canister_id','protocol','op','tick','abstract','amt','max','lim',
                # 'create_time','update_time'
        )
        article_id_list = []
        # datetime.datetime(2023, 12, 23, 15, 45, 28, 715241, tzinfo=datetime.timezone.utc)}
        # print('')
        # count = article_list_model.count()
        # print('--article_list_model--',article_list_model,self.get_type_name(article_list_model),'-count-',count )
        # --article_list_model-- <QuerySet [<article_list: article_list object (4)>]> QuerySet -count- 1
        # --article_list_model-- <QuerySet [{'id': 1, 'article_id': '0C06JCQHBT5NXWCHPDKG7C18C9'}, {'id': 2, 'article_id': '0C06EDN154324KZER2JTHM9P0A'}]> QuerySet -count- 2
        # --article_list_model-- <QuerySet []> QuerySet
        article_exist_id_list = [ t['article_id'] for t in article_list_model]
        article_list_model = []


        # install_article_data = []
        obj_install_data = []
        for index, row in enumerate(multi_data):
            # print('')
            article_id = row['id']
            if article_id not in article_exist_id_list:
                # -id- {'id': '0C09WWSKTPZRY4J0YQC75RX791', 'status': {'Public': None}, 'thumb': 'QmVtDL4UyJjHUae8b6vESaimb59kebprkagMmawE2HSUiq', 'title': 'MORA', 'created': 1702054651571, 'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 'cate': 0, 'like': 0, 'tags': [], 'view': 0, 'fromurl': '', 'unlike': 0, 'author': 'e2yd5-tlpth-eejos-g6v5h-irhiw-urz74-qdvdx-skpmm-7o3c3-jcbrn-iae', 'commentTotal': 0, 'comment': 0, 'updated': 1702054651571, 'abstract': 'Mint: { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" }\n', 'allowComment': False, 'copyright': [], 'original': True, 'commentNew': 0, 'user_canister_id': 't6etm-yyaaa-aaaan-qdb6q-cai', 'canister_index': 8, 'page': 2, 'op_tick_group_key': 'mint_mora', 'abstract_json': {'p': 'mora-20', 'op': 'mint', 'tick': 'mora', 'amt': '1000'}}
                # print('-id-',row.get('id'), row.get('thumb'), row.get('title'),row.get('created'),row.get('updated'),row.get('toped'),row.get('subcate'))
                # print('-cate-',row.get('cate'), row.get('like'),row.get('view'),row.get('fromurl'),row.get('unlike'),row.get('commentTotal'),row.get('abstract')  )
                # print('-commentTotal-',row.get('commentTotal'),row.get('comment'), row.get('allowComment'),row.get('original'),row.get('commentNew'),row.get('author'),row.get('user_canister_id'))
                # print('')
                # print('-abstract_json-',row.get('abstract_json'), self.get_type_name(row.get('abstract_json'))  )
                tags = row.get('tags')
                copyright = row.get('copyright')
                atype_dict = row.get('atype')
                status_dict = row.get('status')
                # print('-status-',status_dict,atype_dict,tags ,copyright  )
                status_public = 'Public' if 'Public' in status_dict else ''
                status_public = 'Subcribe' if 'Subcribe' in status_dict and not status_public else status_public
                status_public = 'Private' if 'Private' in status_dict and not status_public else status_public
                status_public = 'Draft' if 'Draft' in status_dict and not status_public else status_public
                status_public = 'Delete' if 'Delete' in status_dict and not status_public else status_public
                # Subcribe:null;Private:null;Draft:null;Public:null;Delete:null
                # print('-status_dict-',status_public  )
                # print('')
                # Photos; Article; Shortle; Audio; Video
                status_atype = 'Article' if 'Article' in atype_dict else ''
                status_atype = 'Photos' if 'Photos' in atype_dict and not status_atype else status_atype
                status_atype = 'Shortle' if 'Shortle' in atype_dict and not status_atype else status_atype
                status_atype = 'Audio' if 'Audio' in atype_dict and not status_atype else status_atype
                status_atype = 'Video' if 'Video' in atype_dict and not status_atype else status_atype
                # print('-status_atype-',status_atype  )

                # abstract_json = row.get('abstract_json')
                # print('-abstract_json-',abstract_json  )
                # 将数据转换为JSON格式
                json_tags = ''
                if tags:
                    json_tags = json.dumps(tags,ensure_ascii=False)
                json_copyright = ''
                if copyright:
                    json_copyright = json.dumps(copyright,ensure_ascii=False)
                
                # print('-json_tags-',json_tags , self.get_type_name(json_tags)  )
                # print('-json_copyright-',json_copyright , self.get_type_name(json_copyright)  )
                # print('')
                # print('')
                data = ArticleListModel(
                    article_id = row.get('id'),
                    article_status = status_public,
                    thumb = row.get('thumb'),
                    title =  row.get('title'),
                    # import datetime
                    # created = 1609459200000  # 示例毫秒时间
                    # 1609459200123
                    # dt = datetime.datetime.fromtimestamp(created / 1000.0)    
                    created =  row.get('created'),
                    updated =  row.get('updated'),
                    # - 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807

                    toped =  row.get('toped'),
                    subcate =  row.get('subcate'),
                    atype =  status_atype,
                    cate =  row.get('cate'),
                    like =  row.get('like'),
                    tags =  json_tags,
                    view = row.get('view'),
                    fromurl = row.get('fromurl'),
                    unlike = row.get('unlike'),
                    comment_total = row.get('commentTotal'),
                    comment = row.get('comment'),
                    allow_comment = row.get('allowComment'),
                    copyright = json_copyright,
                    original = row.get('original'),
                    comment_new = row.get('commentNew'),

                    author = row.get('author'),
                    canister_id = row.get('user_canister_id'),

                    # {'p': 'mora-20', 'op': 'mint', 'tick': 'mora', 'amt': '1000'}
                    protocol = row.get('protocol'),
                    op = row.get('op'),
                    tick = row.get('tick'),

                    abstract = row.get('abstract'),

                    amt = row.get('amt') if 'amt' in row else 0,
                    max = row.get('max') if 'max' in row else 0,
                    lim = row.get('lim') if 'lim' in row else 0,


                    # create_time = create_time,      # 入库创建时间 
                    # update_time = create_time,      # 入库更新时间

                )
                obj_install_data.append(data)
                # install_article_data.append(item)
            # print('--article--item--',item)
            del multi_data[index]
        # print('--install_article_data--',len(install_article_data) ,self.get_type_name(install_article_data) )

        if obj_install_data:
            ArticleListModel.objects.bulk_create(obj_install_data)
        obj_install_data = []
        # # 删除数据
        # exist_id_list = [ t['id'] for t in article_list_model]
        # print('')
        # print('--exist_id_list--',exist_id_list)
        # ArticleListModel.objects.filter(pk__in=exist_id_list).delete()

        # # 创建 10 个 Person 对象并使用 bulk_create() 方法保存到数据库中
        # people = [Person(name=f"Person {i}", age=random.randint(1, 100)) for i in range(10)]
        # Person.objects.bulk_create(people)

        # # 将列表中的数据转换为 MyModel 对象列表
        #     my_model_objects = [
        #         MyModel(
        #             field1=row[0],
        #             field2=row[1],
        #             # ...
        #         )
        #         for row in data
        #     ]
        #     # 批量插入到数据库中
        #     MyModel.objects.bulk_create(my_model_objects)
        # objs = [
        #     MyModel(name='John', age=30),
        #     MyModel(name='Mary', age=25),
        #     MyModel(name='Peter', age=40),
        # ]
        # MyModel.objects.bulk_create(objs)

    def calculate_total_pages(self,limit, total):  
        """  
        计算总页数  
        :param elements_per_page: 每页包含的数量  
        :param total_elements: 总数量  
        :return: 总页数  
        """  
        total_pages = math.ceil(total / limit)  
        return total_pages
    def canister_article_is_exists(self,canister_id:str='',canister_index='0',article_id:str='',page='0'):
        ''' 
        检测同一个 canister_id 下的文章ID是否存在文件 
        这种用文件检测 如果同时并发 是否有问题 如果有问题是否可以转移到redis
        '''

        canister_id_path = os.path.join(self.canister_id_article_id_is_exists_path, canister_id)
        mk_dir(canister_id_path)
        # 判断这个文件是否存在 
        canister_article_id_path = os.path.join(canister_id_path, "{}.json".format(article_id) )
        file_is_exist = file_python_exists(canister_article_id_path)
        tmp_op_tick_group_dict = {
            "canister_id":canister_id,
            "canister_index":canister_index,
            "article_id":article_id,
            "page":page,
        }

        if file_is_exist:
            # 去重
            tmp_op_tick_group_dict['追加'] = 'canister_article_path_append'
            print('')
            show_msg = '--检测同一个 canister_id 下的文章ID是否存在文件 article_id:{} page:{} canister_id:{} canister_index:{} canister_article_id_path:{}'.format(article_id, page,canister_id ,canister_index,canister_article_id_path)
            print( show_msg )
            print('')
            append_to_jsonl(file_path=canister_article_id_path, data=tmp_op_tick_group_dict)
        else:
            tmp_op_tick_group_dict['22222'] = '检测同一个 canister_id 下的文章ID是否存在文件'
            append_to_jsonl(file_path=canister_article_id_path, data=tmp_op_tick_group_dict)
        return file_is_exist

    def thread_pool_articles(self,user_canister_id = '',canister_index=0):
        ''' 获取总条数 再用线程池 '''
        user_governance = Canister(agent=self.agent, canister_id=user_canister_id, candid=self.user_governance_did)
        # 目前最大只能是50
        size = 50
        canister_article_list = []
        page = 1
        # 传的参数必须每个格式都正确
        queryArticleReq = {
            # 发布状态 枚举[variant]  多选一  Subcribe:null;Private:null;Draft:null;Public:null;Delete:null
            "status":[{'Public':None}], "subcate":0
            , "atype":[{"Article":None}], "cate":0,
            # 第几页
            "page":page,
            # 每一页展示多少条数据   # 时间倒序排序            # 搜索 'title': 'ICLANDLORD'    'title': 'title_22' 区分大小写
            "size":size,              "sort":{"TimeDesc":None},"search":""
        }
        res = user_governance.queryArticles(queryArticleReq)
        ret = res[0]
        article_id_dict = {}
        ret_list_data = ret.get('data',[]) or []
        # page = ret.get('page',0) or 0
        self.make_canister_article_page_list(ret_list_data,user_canister_id,canister_index,page)
        queryArticleReq = {}
        user_governance = {}
        '''
        for item_line in ret_list_data:
            # 当前canister_id 根据文章id去重
            # self.canister_id_article_id_is_exists_path
            # if item_line['id'] in article_id_dict:
            #     continue
            if self.canister_article_is_exists(user_canister_id,canister_index,item_line['id'],page):
                continue
            
            item_line['user_canister_id'] = user_canister_id
            item_line['canister_index'] = canister_index
            # TypeError: Object of type Principal is not JSON serializable
            item_line['author'] = item_line['author'].to_str()
            item_line['page'] = page

            # -abstract- Mint: { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" }
            # -abstract- Mora Protocol
            abstract = item_line['abstract']
            # python 去除字符串右边的换行符
            abstract = abstract.rstrip('\n')
            abstract = abstract.rstrip('\r')
            abstract = abstract.rstrip('\r\n')
            
            #  python 检测字符串是否为Mint: {开头的
            if abstract.startswith('Mint:'):
                # print("该字符串以 'Mint: {' 开头")
                # 删除字符串左边的特定字符
                new_s = abstract.lstrip('Mint:')
                items_line = self.op_tick_group_data_make(item_line,user_canister_id,new_s,abstract)
                if items_line:
                    # print('--item_line--',item_line,self.get_type_name(item_line))
                    # 记录每一行不重复的数据
                    # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                    canister_article_list.append(items_line)

                    # self.save_article_dict_info(items_line)

                    # article_id_dict[items_line['id']] = items_line['id']
                    
                # new_s = new_s.lstrip(' ')
                # # -new_s- { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" } tag：$mora
                # if new_s.__contains__(' tag：'):
                #     new_s_list = new_s.split(' tag：')
                #     new_s = new_s_list[0]
                # # -new_s- { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" }.
                # new_s = new_s.rstrip('.')
                # print('-new_s-',user_canister_id,"kkk{}ppp".format(new_s) )
                # try:
                #     abstract_json = json.loads(new_s)
                #     print('-abstract_json-',abstract_json,'type=',self.get_type_name(abstract_json) )
                #     article_id = item_line['id'] 
                #     op_tick_group_key = '{}_{}'.format(abstract_json['op'],abstract_json['tick'])
                #     # 加组
                #     item_line[op_tick_group_key] = op_tick_group_key
                #     self.op_tick_group_data_dict[op_tick_group_key] = {}
                #     # 去重
                #     # self.op_tick_group_data_dict[op_tick_group_key][article_id] = item_line
                #     if article_id in self.op_tick_group_data_dict[op_tick_group_key]:
                #         self.op_tick_group_data_dict[op_tick_group_key][article_id]['count'] += 1
                #     else:
                #         self.op_tick_group_data_dict[op_tick_group_key][article_id] = {
                #             "count":1,
                #             "item_line":item_line,
                #         }
                #     # print('--item_line--',item_line,self.get_type_name(item_line))
                #     # 记录每一行不重复的数据
                #     # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                #     canister_article_list.append(item_line)
                #     article_id_dict[item_line['id']] = 1
                # except:
                #     print('-abstract error Mint -',user_canister_id,"kkk{}ppp".format(abstract) )
            elif abstract.startswith('Deploy:'):
                # print("该字符串以 'Deploy: {' 开头")
                # print('-abstract-',abstract)
                # 删除字符串左边的特定字符
                new_s = abstract.lstrip('Deploy:')
                items_line = self.op_tick_group_data_make(item_line,user_canister_id,new_s,abstract)
                if items_line:
                    # print('--item_line--',item_line,self.get_type_name(item_line))
                    # 记录每一行不重复的数据
                    # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                    # self.op_deploy_tick_group_data_make(items_line)
                    canister_article_list.append(items_line)
                    # article_id_dict[items_line['id']] = items_line['id']
                    
                # new_s = new_s.lstrip(' ')
                # print('-new_s-',new_s)
                # abstract_json = json.loads(new_s)
                # print('-abstract_json-',abstract_json,'type=',self.get_type_name(abstract_json) )
                # article_id = item_line['id'] 
                # op_tick_group_key = '{}_{}'.format(abstract_json['op'],abstract_json['tick'])
                # self.op_tick_group_data_dict[op_tick_group_key] = {}
                # self.op_tick_group_data_dict[op_tick_group_key][article_id] = item_line
                # # print('--item_line--',item_line,self.get_type_name(item_line))
                # # 记录每一行不重复的数据
                # # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                # canister_article_list.append(item_line)
                # article_id_dict[item_line['id']] = 1
            else:
                pass
                # print("该字符串不以 '{' 开头",abstract)
        '''




        hasmore = ret.get('hasmore',False) or False
        data_list_len = len(ret.get('data',[]) or [])
        if not hasmore:
            # msg = f'_________________thread_pool_articles 数据取完了-只有这一页数据了 user_canister_id={user_canister_id}  canister_index={canister_index}  data_list_len={data_list_len}'
            # print(msg)
            # item_line = {
            #     "msg":msg
            # }
            # append_to_jsonl(file_path=self.indes_canister_data_dict_path, data=item_line)
            # 清空数据
            article_id_dict = {}
            # 只有这一页数据了
            return canister_article_list
        
        total = ret.get('total',0) or 0
        if not total:
            return []
        
        ret = {}
        ret_list_data = []
        res = []


        #     with map_httpcore_exceptions():
        # File "D:\python\3.10.9\lib\contextlib.py", line 153, in __exit__
        #     self.gen.throw(typ, value, traceback)
        # File "F:\project\env_pip_dir\ic_principal\lib\site-packages\httpx\_transports\default.py", line 83, in map_httpcore_exceptions
        #     raise mapped_exc(message) from exc
        # httpx.ConnectTimeout: _ssl.c:980: The handshake operation timed out

        # 'total': 835
        # for page in range(1,total+1):
        #     print(page)
        # 根据总条数计算总页数
        total_page = self.calculate_total_pages(size,total)
        # inclusive_range = list(range(2, total_page + 1)) 
        total = 0

        max_worker = 100
        # msg = f'----------------------------------- thread_pool_articles  user_canister_id={user_canister_id} canister_index={canister_index} total={total} inclusive_range={inclusive_range}'
        # print(msg)
        # item_line = {
        #     "msg":msg
        # }
        # append_to_jsonl(file_path=self.indes_canister_data_dict_path, data=item_line)
        # for page in range(2,total_page+1):
        #     # print('Index: {}, canister_id: {}'.format(page, user_canister_id))
        #     obj = self.query_user_articles(user_canister_id,page,canister_index)

        with ThreadPoolExecutor(max_workers=max_worker) as t:
            obj_list = []
            for page in range(2,total_page+1):
                # print('Index: {}, canister_id: {}'.format(page, user_canister_id))
                obj = t.submit(self.query_user_articles, user_canister_id,page,canister_index)
                # obj_list.append(obj)
            '''
            for future in as_completed(obj_list):
                ret_data = future.result()
                ret_list_data = ret_data.get('data',[]) or []
                page = ret_data.get('page',0) or 0
                for item_line in ret_list_data:
                    # 当前canister_id 根据文章id去重
                    # if item_line['id'] in article_id_dict:
                    #     # print("--------item_line['id'] in article_id_dict-------",item_line['id'],'',article_id_dict[item_line['id']])
                    #     continue
                    if self.canister_article_is_exists(user_canister_id,canister_index,item_line['id'],page):
                        continue
                    item_line['user_canister_id'] = user_canister_id
                    item_line['canister_index'] = canister_index
                    item_line['page'] = page
                    item_line['author'] = item_line['author'].to_str()
                    # -abstract- Mint: { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" }
                    # -abstract- Mora Protocol
                    abstract = item_line['abstract']
                    # python 去除字符串右边的换行符
                    abstract = abstract.rstrip('\n')
                    abstract = abstract.rstrip('\r')
                    abstract = abstract.rstrip('\r\n')
                    # 是否有 Mint: {
                    if abstract.startswith('Mint:'):
                        # print("该字符串以 'Mint: {' 开头")
                        new_s = abstract.lstrip('Mint:')
                        items_line = self.op_tick_group_data_make(item_line,user_canister_id,new_s,abstract)
                        if items_line:
                            # print('--item_line--',item_line,self.get_type_name(item_line))
                            # 记录每一行不重复的数据
                            # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                            # pass
                            canister_article_list.append(items_line)

                            # article_id_dict[items_line['id']] = items_line['id']
                            
                    elif abstract.startswith('Deploy:'):
                        # print("该字符串以 'Deploy: {' 开头")
                        # print('-abstract-',abstract)
                        # 删除字符串左边的特定字符
                        new_s = abstract.lstrip('Deploy:')
                        items_line = self.op_tick_group_data_make(item_line,user_canister_id,new_s,abstract)
                        if items_line:
                            # print('--item_line--',item_line,self.get_type_name(item_line))
                            # 记录每一行不重复的数据
                            # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                            # self.op_deploy_tick_group_data_make(items_line)
                            canister_article_list.append(items_line)
                            # article_id_dict[items_line['id']] = items_line['id']
                        
                            
                        # new_s = new_s.lstrip(' ')
                        # print('-new_s-',new_s)
                
                        # abstract_json = json.loads(new_s)
                        # print('-abstract_json-',abstract_json,'type=',self.get_type_name(abstract_json) )
                        # article_id = item_line['id'] 
                        # op_tick_group_key = '{}_{}'.format(abstract_json['op'],abstract_json['tick'])
                        # self.op_tick_group_data_dict[op_tick_group_key] = {}
                        # self.op_tick_group_data_dict[op_tick_group_key][article_id] = item_line

                        # # print('--item_line--',item_line,self.get_type_name(item_line))
                        # # 记录每一行不重复的数据
                        # # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                        # canister_article_list.append(item_line)
                        # article_id_dict[item_line['id']] = 1
                    else:
                        pass
                        # print("该字符串不以 '{' 开头",abstract)
                # if ret_data:
                #     canister_article_list.append(ret_data)
                    # print("返回的",ret_data)
            '''
        # 清空数据
        article_id_dict = {}
        return canister_article_list
    def save_article_dict_info(self,article_item:dict={}):
        pass
    def op_deploy_tick_group_data_make(self,item_line):
        ''' op是deploy的根据tick分组统计 '''
        
        # self.op_deploy_tick_group_data_list_path = os.path.join(self.json_data_path, 'op_deploy_tick_group_data_list_path.jsonl')
        # self.op_deploy_tick_group_data_dict = {
        #     "icps":{
        #         # 总供应
        #         "max_supply":0,
        #         # 持有人数-去重author
        #         "holders":0,
        #         # 如果当前文章abstract的值是deploy 就取当前文章的created字段
        #         "create":"",
        #         # 进度 当前mint的数量/总供应 [每一张铭文{文章}的amt是1000 当第21个被mint那进度就是100%]
        #         "progress":"",
        #         # 分组固定值
        #         "tick":"icps",
        #         # 当前文章 abstract 下的 amt 值
        #         "amt":"",
        #         # 当前文章 abstract 下的 op 值
        #         "op":"deploy",
        #         # 当前文章 abstract 下的 p值
        #         "protocol":"",
        #         # "":"",
        #     },
        # }
        
        abstract_json = item_line['abstract_json']
        op = abstract_json['op']
        if 'deploy' != op:
            return {}

        tick = abstract_json['tick']
        max = abstract_json['max']
        p = abstract_json['p']
        lim = abstract_json['lim']

        # print('')
        # print('==op_deploy_tick_group_data_make==',item_line['user_canister_id'],item_line['created'],item_line['abstract'],item_line['op_tick_group_key'],item_line['id'],max)
        # The handshake operation timed out
        # httpx.ReadTimeout: The read operation timed out
        '''
        {
            'id': '0C9YCESX6J5TV183NEX5G1DPCJ', 'status': {'Public': None}, 'thumb': 'QmeVYdJ4jvV6GcHbE7DdMaNowU2WsnNTibGRkw4oswnWui', 'title': 'FKDOM', 'created': 1702386004349, 
            'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 'cate': 0, 'like': 0, 'tags': [], 'view': 0, 'fromurl': '', 'unlike': 0, 
            'author': 'ycaq2-am5es-7ddcs-u5keb-5xawp-k4d3w-tsilc-hd2fk-tiuy4-wopfn-jae', 'commentTotal': 0, 'comment': 0, 'updated': 1702386028053, 
            'abstract': 'Deploy: { "p": "mora-20", "op": "deploy", "tick": "fkdom", "max": "2100", "lim": "1" } ', 'allowComment': False, 'copyright': [], 'original': True, 
            'commentNew': 0, 'user_canister_id': 'tcaj5-pyaaa-aaaan-qdb4q-cai', 'canister_index': 4, 'page': 1, 'op_tick_group_key': 'deploy_fkdom', 
            'abstract_json': {'p': 'mora-20', 'op': 'deploy', 'tick': 'fkdom', 'max': '2100', 'lim': '1'}
        }
        
        if tick not in self.op_deploy_tick_group_data_dict:
            self.op_deploy_tick_group_data_dict[tick] = {
                # 总供应
                "max_supply":0,
                # 持有人数-去重author
                "holders":0,
                "holders_dict":{},
                # 如果当前文章abstract的值是deploy 就取当前文章的created字段
                "create":item_line['created'],
                # 进度 当前mint的数量/总供应 [每一张铭文{文章}的lim是1000 当第21个被mint那进度就是100%]
                "progress":"",
                # 分组固定值
                "tick":tick,
                # 当前文章 abstract 下的 lim 值
                "lim":lim,
                # 当前文章 abstract 下的 op 值
                "op":op,
                # 当前文章 abstract 下的 p值
                "protocol":p,
            }

        self.op_deploy_tick_group_data_dict[tick]['max_supply'] += int(max)
        # self.op_deploy_tick_group_data_dict[tick]['holders_dict'][item_line['author']] = 1
        # self.op_deploy_tick_group_data_dict[tick]['holders'] = len(self.op_deploy_tick_group_data_dict[tick]['holders_dict'])
        '''
        

    def op_tick_group_data_make(self,items_line,user_canister_id,new_s,abstract):
        ''' 处理每一个文章的格式 '''
        # print("该字符串以 'Mint: {' 开头")
        # print("该字符串以 'Deploy: {' 开头")
        # print('-abstract-',abstract)
        # 删除字符串左边的特定字符
        # new_s = abstract.lstrip('Mint:')
        # new_s = abstract.lstrip('Deploy:')
        new_s = new_s.strip(' ')
        
        # -new_s- { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" } tag：$mora
        if new_s.__contains__(' tag：'):
            new_s_list = new_s.split(' tag：')
            new_s = new_s_list[0]
        new_s = new_s.rstrip('.')
        # print('-new_s __contains__-',user_canister_id,"aaa{}zzz".format(new_s) )
        # -new_s- kkk{ "p": "mora-20", "op": "mint", "tick": "nnsdao", "amt": "1000" ppp
        article_id = items_line['id']
        try:
            abstract_json = json.loads(new_s)
            # print('-abstract_json-',abstract_json,'type=',self.get_type_name(abstract_json) )
            
            op_tick_group_key = '{}_{}'.format(abstract_json['op'],abstract_json['tick'])
            # 加组
            items_line['op_tick_group_key'] = op_tick_group_key
            # items_line['abstract_json'] = abstract_json
            items_line["protocol"]=abstract_json["p"]
            items_line["op"]=abstract_json["op"]
            items_line["tick"]=abstract_json["tick"]
            items_line["amt"]= int(abstract_json["amt"]) if 'amt' in abstract_json else 0
            items_line["max"]=int(abstract_json["max"]) if 'max' in abstract_json else 0
            items_line["lim"]=int(abstract_json["lim"]) if 'lim' in abstract_json else 0
            

            # ------make_canister_article_page_list----- {'id': '0C6ADX4T9D3F10GA4KAMH4V4VD', 'status': {'Public': None}, 'thumb': 'QmUgfHX5Z7gqncCvhUuWQeSPeH4vWUBBTbHwgbQ1aGLSTT', 'title': 'Power', 'created': 1702261404722, 'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 'cate': 0, 'like': 0, 'tags': [], 'view': 0, 'fromurl': '', 'unlike': 0, 'author': 'r3257-akxyo-m7uo5-ifsx2-bgjzk-hk6zj-da2w4-andpt-zs4xz-y5v3d-sae', 'commentTotal': 0, 'comment': 0, 'updated': 1702261404722, 'abstract': 'Mint:{"p":"mora-20","op":"mint","tick":"power","amt":"likes"}', 'allowComment': True, 'copyright': [], 'original': True, 'commentNew': 0, 'user_canister_id': 'erpbi-cyaaa-aaaan-qdccq-cai', 'canister_index': 16, 'page': 1, 'op_tick_group_key': 'mint_power', 'protocol': 'mora-20', 'op': 'mint', 'tick': 'power', 'amt': 'likes', 'max': 0, 'lim': 0}
            # op_tick_article_id_key = "{}_{}".format(op_tick_group_key,article_id)
            # key 去重
            # self.op_tick_article_id_key_dict[op_tick_group_key] = {}
            # if op_tick_group_key not in self.op_tick_article_id_key_dict:
            #     self.op_tick_article_id_key_dict[op_tick_group_key] = {}
            
            # if op_tick_group_key not in self.op_tick_group_data_dict:
            #     self.op_tick_group_data_dict[op_tick_group_key] = []
            tmp_op_tick_group_dict = {
                "op_tick_article_id_去重.key_dic":op_tick_group_key,
                "canister_id":items_line['user_canister_id'],
                "canister_index":items_line['canister_index'],
                "article_id":article_id,
                "page":items_line['page'],
            }
            op_tick_group_key_path = os.path.join(self.op_tick_group_is_exists_key, op_tick_group_key)
            mk_dir(op_tick_group_key_path)
            # 判断这个文件是否存在 
            op_tick_group_article_id_path = os.path.join(op_tick_group_key_path, "{}.json".format(article_id) )
            file_is_exist = file_python_exists(op_tick_group_article_id_path)

            articl_op_tick_key = '{}_{}'.format(op_tick_group_key,article_id)
            if articl_op_tick_key not in self.op_tick_group_data_dict:
                self.op_tick_group_data_dict[articl_op_tick_key] = items_line
            if file_is_exist:
                # 去重
                tmp_op_tick_group_dict['追加'] = 'op_tick_append'
                print('')
                print('--去重.op_tick_article_id_key_dic]--article_id:{}_op_tick_group_key:{}_page:{}_canister_id:{}_canister_index:{}_op_tick_group_article_id_path:{}'.format(article_id,op_tick_group_key,items_line["page"],items_line['user_canister_id'] ,items_line["canister_index"],op_tick_group_article_id_path)  )
                print('')
                append_to_jsonl(file_path=op_tick_group_article_id_path, data=tmp_op_tick_group_dict)
                # pass
            else:
                tmp_op_tick_group_dict['11111'] = '11111'
                append_to_jsonl(file_path=op_tick_group_article_id_path, data=tmp_op_tick_group_dict)
                # if article_id in self.op_tick_article_id_key_dict[op_tick_group_key]:
                #     append_to_jsonl(file_path=op_tick_group_article_id_path, data=tmp_op_tick_group_dict)
                #     pass
                # else:
                #     append_to_jsonl(file_path=op_tick_group_article_id_path, data=tmp_op_tick_group_dict)
                # key 去重
                # self.op_tick_article_id_key_dict[op_tick_group_key][article_id] = article_id
                # 真正的数据
                '''
                
                items_tmp_line = {
                    "article_id":article_id,
                    "op_tick_group_key":op_tick_group_key,

                    "title":items_line["title"],
                    "created":items_line["created"],
                    "updated":items_line["updated"],
                    "page":items_line["page"],
                    "tags":items_line["tags"],

                    "author":items_line["author"],
                    "canister_id":items_line['user_canister_id'],
                    "canister_index":items_line["canister_index"],
                    
                    "protocol":abstract_json["p"],
                    "op":abstract_json["op"],
                    "tick":abstract_json["tick"],
                    "amt":abstract_json["amt"] if 'amt' in abstract_json else 0,
                    "max":abstract_json["max"] if 'max' in abstract_json else 0,
                    "lim":abstract_json["lim"] if 'lim' in abstract_json else 0,
                    
                }
                '''
                
                # self.op_tick_group_data_dict[op_tick_group_key].append(items_line)
                # self.op_tick_group_data_dict.append(items_line)
            # self.op_tick_article_id_key_dict[op_tick_article_id_key] = article_id
            # self.op_tick_group_data_dict[op_tick_group_key] = {}
            # 去重
            # self.op_tick_group_data_dict[op_tick_group_key][article_id] = items_line
            # if article_id in self.op_tick_group_data_dict[op_tick_group_key]:
            #     self.op_tick_group_data_dict[op_tick_group_key][article_id]['count'] += 1
            # else:
            #     self.op_tick_group_data_dict[op_tick_group_key][article_id] = {
            #         "count":1,
            #         "item_line":items_line,
            #     }


            # print('--item_line--',items_line,self.get_type_name(items_line))
            # 记录每一行不重复的数据
            # append_to_jsonl(file_path=self.all_data_list_path, data=items_line)
            # canister_article_list.append(items_line)
            # article_id_dict[items_line['id']] = items_line['id']
        except:
            # -abstract error __contains__- tcaj5-pyaaa-aaaan-qdb4q-cai abstract aaaDeploy: { "p": "mora-20", "op": "deploy", "tick": "fkdom", "max": "2100", "lim": "1" } zzz
            # print('-abstract error __contains__-',user_canister_id,"abstract aaa{}zzz id={}".format(abstract,article_id) )
            items_line = {}
        return items_line
    def save_config_json(self,config_path,config_dict_data):
        # 将 config_dict_data 保存到json文件中
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict_data, f, ensure_ascii=False)
    def query_user_articles(self,user_canister_id = '',page=1,canister_index=0):
        ''' 根据用户-分页返回文章-不同的页数据可能重复 '''
        # 暂停一下 线程池速度太快接口会超时
        time.sleep(1)
        # msg = f'======================================query_user_articles  user_canister_id={user_canister_id}  canister_index={canister_index}  page={page}'
        # print(msg)
        # item_line = {
        #     "msg":msg
        # }
        # append_to_jsonl(file_path=self.indes_canister_data_dict_path, data=item_line)
    
        # return {}
    
        # Index: 10311, Value: ecj4r-myaaa-aaaan-qja5q-cai
        user_governance = Canister(agent=self.agent, canister_id=user_canister_id, candid=self.user_governance_did)
        # time_total_current = getTime()
        # formatted_total_start_time = time_total_current['formatted_time']
        # forma_ted_total_start_time = time_total_current['forma_ted_time']
        # 目前最大只能是50
        size = 50

        # time.sleep(3)
        # time_current = getTime()
        # formatted_start_time = time_current['formatted_time']
        # forma_ted_start_time = time_current['forma_ted_time']

        # print('user_canister_id=',user_canister_id,'page=',page)
        # 传的参数必须每个格式都正确
        queryArticleReq = {
            # 发布状态 枚举[variant]  多选一  Subcribe:null;Private:null;Draft:null;Public:null;Delete:null
            "status":[{'Public':None}], "subcate":0
            , "atype":[{"Article":None}], "cate":0,
            # 第几页
            "page":page,
            # 每一页展示多少条数据   # 时间倒序排序            # 搜索 'title': 'ICLANDLORD'    'title': 'title_22' 区分大小写
            "size":size,              "sort":{"TimeDesc":None},"search":""
        }
        res = user_governance.queryArticles(queryArticleReq)
        # httpx.ReadTimeout: The read operation timed out
        # httpx.ConnectTimeout: _ssl.c:980: The handshake operation timed out
        ret = res[0]
        hasmore = ret.get('hasmore',False) or False
        data_list_len = len(ret.get('data',[]) or [])
        total = ret.get('total',0) or 0
        ret_list_data = ret.get('data',[]) or []
        self.make_canister_article_page_list(ret_list_data,user_canister_id,canister_index,page)
        ret = {}
        ret_list_data = []
        res = []
        queryArticleReq = {}
        user_governance = {}
        
        # page = ret.get('page',0) or 0
        # del ret['data']
        # if not hasmore:
        #     print('user_canister_id=',user_canister_id,'page=',page,'数据取完了','data_list_len=',data_list_len,ret)
        #     return {}
        # print('======================================','query_user_articles','user_canister_id=',user_canister_id,'canister_index=',canister_index,'len=',len(ret),'total=',total,'data_list_len=',data_list_len,'page=',page)
        # msg = f'====================================== query_user_articles  user_canister_id={user_canister_id}  canister_index={canister_index}  page={page} len={len(ret)} total={total} data_list_len={data_list_len} page={page}'
        # print(msg)
        # item_line = {
        #     "msg":msg
        # }
        # append_to_jsonl(file_path=self.indes_canister_data_dict_path, data=item_line)

        
        # time_end_current = getTime()
        # formatted_end_time = time_end_current['formatted_time']
        # forma_ted_end_time = time_end_current['forma_ted_time']
        # print( 'data=',ret, 'len=',len(res),'type=',get_type_name(res) ,'formatted_start_time=',formatted_start_time,'formatted_end_time=',formatted_end_time,'data_list_len=',data_list_len )
        # time_total_end_current = getTime()
        # formatted_total_end__time = time_total_end_current['formatted_time']
        # # forma_ted_total_end__time = time_total_end_current['forma_ted_time']
        # print( 'formatted_total_start_time=',formatted_total_start_time, 'formatted_total_end__time=',formatted_total_end__time )

        # inclusive_range = list(range(2, total + 1)) 
        # print(inclusive_range)

        # if ret_data:
        #     canister_article_list.append(ret_data)
            # print("返回的",ret_data)
        # return ret
        return []
    def make_canister_article_page_list(self,ret_list_data,user_canister_id,canister_index,page):
        ''' 处理每一页的数据 '''
        multi_data_list = []
        # for item_line in ret_list_data:
        for index, item_line in enumerate(ret_list_data):
            # 当前canister_id 根据文章id去重
            # if item_line['id'] in article_id_dict:
            #     # print("--------item_line['id'] in article_id_dict-------",item_line['id'],'',article_id_dict[item_line['id']])
            #     continue
            if self.canister_article_is_exists(user_canister_id,canister_index,item_line['id'],page):
                # 删除多余的数据
                del ret_list_data[index]
                continue
            item_line['user_canister_id'] = user_canister_id
            item_line['canister_index'] = canister_index
            item_line['page'] = page
            item_line['author'] = item_line['author'].to_str()


            # -abstract- Mint: { "p": "mora-20", "op": "mint", "tick": "mora", "amt": "1000" }
            # -abstract- Mora Protocol
            abstract = item_line['abstract']
            # python 去除字符串右边的换行符
            abstract = abstract.rstrip('\n')
            abstract = abstract.rstrip('\r')
            abstract = abstract.rstrip('\r\n')
            # 是否有 Mint: {
            if abstract.startswith('Mint:'):
                # print("该字符串以 'Mint: {' 开头")
                new_s = abstract.lstrip('Mint:')
                items_line = self.op_tick_group_data_make(item_line,user_canister_id,new_s,abstract)
                if items_line:
                    
                    # print('--item_line--',item_line,self.get_type_name(item_line))
                    # 记录每一行不重复的数据
                    # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                    # pass
                    # print('')
                    # print('------make_canister_article_page_list-----',items_line)
                    try:
                        items_line["amt"] = int(items_line["amt"])
                        multi_data_list.append(items_line)
                    except:
                        pass

                    # article_id_dict[items_line['id']] = items_line['id']

            elif abstract.startswith('Deploy:'):
                # print("该字符串以 'Deploy: {' 开头")
                # print('-abstract-',abstract)
                # 删除字符串左边的特定字符
                new_s = abstract.lstrip('Deploy:')
                items_line = self.op_tick_group_data_make(item_line,user_canister_id,new_s,abstract)
                if items_line:
                    # print('--item_line--',item_line,self.get_type_name(item_line))
                    # 记录每一行不重复的数据
                    # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                    # self.op_deploy_tick_group_data_make(items_line)
                    # print('')
                    # print('------make_canister_Deploy_article_page_list-----',items_line)
                    # multi_data_list.append(items_line)
                    try:
                        items_line["amt"] = int(items_line["amt"])
                        multi_data_list.append(items_line)
                    except:
                        pass

                    # article_id_dict[items_line['id']] = items_line['id']
                
                    
                # new_s = new_s.lstrip(' ')
                # print('-new_s-',new_s)
        
                # abstract_json = json.loads(new_s)
                # print('-abstract_json-',abstract_json,'type=',self.get_type_name(abstract_json) )
                # article_id = item_line['id'] 
                # op_tick_group_key = '{}_{}'.format(abstract_json['op'],abstract_json['tick'])
                # self.op_tick_group_data_dict[op_tick_group_key] = {}
                # self.op_tick_group_data_dict[op_tick_group_key][article_id] = item_line

                # # print('--item_line--',item_line,self.get_type_name(item_line))
                # # 记录每一行不重复的数据
                # # append_to_jsonl(file_path=self.all_data_list_path, data=item_line)
                # canister_article_list.append(item_line)
                # article_id_dict[item_line['id']] = 1
            else:
                pass
                # print("该字符串不以 '{' 开头",abstract)
            # 删除多余的数据
            del ret_list_data[index]
        self.multi_save_op_tick_list_to_db(multi_data_list)
        self.multi_save_article_list_to_db(multi_data_list)
        multi_data_list = []

def getTime():
    # 获取当前日期和时间
    now = datetime.datetime.now()
    # 格式化日期和时间
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    forma_ted_time = now.strftime("%Y-%m-%d_%H%M%S")
    return {"formatted_date":formatted_date,"formatted_time":formatted_time,"forma_ted_time":forma_ted_time}
# def get_root():
#     return os.path.dirname(os.path.abspath(__file__))

def mk_dir(path):
    ''' 创建目录 '''
    # 引入模块
    # import os

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        # print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path+' 目录已存在')
        return False
def remove_folder(path):
    ''' 会直接删除整个文件夹及其内容.在使用方法2时,需要确保路径有效性,以免意外删除其他文件夹 '''
    if os.path.exists(path):
        shutil.rmtree(path)
def file_python_exists(file_path):
    return os.path.exists(file_path)
def append_to_jsonl(file_path, data):
    # 将数据转换为JSON格式  
    json_data = json.dumps(data,ensure_ascii=False)
  
    # 追加写入到.jsonl文件中  
    with open(file_path, 'a',encoding='utf-8') as file:  
        file.write(json_data + '\n')  

def run():
    # obj = ic_data_statistics()
    # formatted_total_start_time= 2023-12-17 23:53:19 formatted_total_end_time= 2023-12-17 23:55:50
    # ret = obj.query_canister_ids()
    # formatted_total_start_time= 2023-12-17 23:56:53 formatted_total_end_time= 2023-12-17 23:57:47
    # ret = obj.thread_pool_data()

    # obj.query_user_articles(user_canister_id='tcaj5-pyaaa-aaaan-qdb4q-cai')
    # obj.query_user_articles(user_canister_id=obj.my_canister_id)
    # ret = obj.thread_pool_articles(user_canister_id='dezyq-kyaaa-aaaan-qdjaa-cai')
    # ret = obj.thread_pool_articles(user_canister_id='ddy6e-haaaa-aaaan-qdjaq-cai')
    print('')
    print('')
    # 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
    # print('--op_tick_group_data_dict--',obj.op_tick_group_data_dict)
    # print('---------------------------目前外部op有deploy,Mint----------下方的统计是根据外部op替换空后转json内部计算-------------------------')
    # for item_group in obj.op_tick_group_data_dict:
    #     print('----------item_group-------',item_group,obj.op_tick_group_data_dict[item_group])
    # print('所有数据地址                ',obj.all_data_list_path)
    # print('op是deploy的根据tick分组统计',obj.op_deploy_tick_group_data_list_path)
    # print('根据op以及tick分组的列表    ',obj.op_tick_group_data_list_path)
    # print('---self.op_deploy_tick_group_data_dict--',obj.op_deploy_tick_group_data_dict)
    # return ret
# if __name__ == "__main__":
#     time_total_current = getTime()
#     formatted_total_start_time = time_total_current['formatted_time']
#     # forma_ted_total_start_time = time_total_current['forma_ted_time']
#     ret = run()

 
#     time_total_end_current = getTime()
#     formatted_total_end_time = time_total_end_current['formatted_time']
#     # forma_ted_total_start_time = time_total_end_current['forma_ted_time']
#     # print(ret)
#     print('formatted_total_start_time=',formatted_total_start_time,'formatted_total_end_time=',formatted_total_end_time)
    


# ic_query_user_articles.py


