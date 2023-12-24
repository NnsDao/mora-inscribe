#!/usr/bin/env python
# -*- coding:utf-8 -*-





# 最顶级可以创建用户的星球
# https://dashboard.internetcomputer.org/canister/53i5d-faaaa-aaaan-qda6a-cai
# https://github.com/rocklabs-io/ic-py


import asyncio
from ic.canister import Canister
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import Types
from ic import Principal

# 类似于Linux的用户
root_canister_id = '53i5d-faaaa-aaaan-qda6a-cai'
user_init_canister_id = 'rrkah-fqaaa-aaaaa-aaaaq-cai'
my_canister_id = 'gkhdz-7yaaa-aaaan-qi2ra-cai'
# efi2f-baaaa-aaaan-qja5a-cai
iden = Identity()
client = Client()
agent = Agent(iden, client)
# read governance candid from file
root_governance_did = open("root_inittrail.did", "r", encoding="utf-8").read()
user_governance_did = open("user_plant.did", "r", encoding="utf-8").read()
# create a governance canister instance
governance = Canister(agent=agent, canister_id=root_canister_id, candid=root_governance_did)

# async call
# async def async_test():
#   res = await governance.list_proposals_async(
#     {
#         'include_reward_status': [], 
#         'before_proposal': [],
#         'limit': 100, 
#         'exclude_topic': [], 
#         'include_status': [1]
#     }
#   )
#   print(res)
# asyncio.run(async_test())



# for user_canister_id in data_list:
#     print('')
#     # f5bpg-paaaa-aaaan-qjaza-cai
#     print(user_canister_id,len(user_canister_id),get_type_name(user_canister_id))
    # query_user_articles(user_canister_id)


def get_type_name(obj):
    ''' 获取类型的名称 '''
    return type(obj).__name__
def query_canister_ids():
    ''' 快照的形式一次性返回全部不重复的id '''
    res = governance.queryCanisterIds()
    data_list = res[0]
    print(  len(data_list),get_type_name(data_list)  )
    for index, value in enumerate(data_list):  
        print('Index: {}, Value: {}'.format(index, value))
        query_user_articles(user_canister_id=value)
def query_user_articles(user_canister_id = ''):
    ''' 根据用户-分页返回文章-不同的页数据可能重复 '''
    # Index: 10311, Value: ecj4r-myaaa-aaaan-qja5q-cai
    principal_a = Principal(b"A")
    print('','principal_a=',principal_a,'principal_a type=',get_type_name(principal_a) ,'principal_a_str=',principal_a.to_str(),'principal_a_str type=',get_type_name(principal_a.to_str() ))
    # self.principal_a = ic.Principal(b"A")
    # self.principal_b = ic.Principal(b"B")



    user_governance = Canister(agent=agent, canister_id=user_canister_id, candid=user_governance_did)
    # record = Types.Record({'foo':Types.Text, 'bar': Types.Int})
    # res = encode([{'type': record, 'value':{'foo': '💩', 'bar': 42}}])

    res = user_governance.get_version()

    # isSubscriber: (principal) -> (QueryCommonSubscriber) query;
    res = user_governance.isSubscriber(principal_a.to_str()) # ValueError: only support string or bytes format
    # res = [{'data': [], 'issubscriber': False}]
    # 传的参数必须每个格式都正确
    queryArticleReq = {
        # 发布状态 枚举[variant]  多选一  Subcribe:null;Private:null;Draft:null;Public:null;Delete:null
        "status":[{'Public':None}], "subcate":0
        , "atype":[{"Article":None}], "cate":0,
        # 第几页
        "page":1,
        # 每一页展示多少条数据   # 时间倒序排序            # 搜索 'title': 'ICLANDLORD'    'title': 'title_22' 区分大小写
        "size":2,              "sort":{"TimeDesc":None},"search":""
    }
    res = user_governance.queryArticles(queryArticleReq)    
    # res = user_governance.queryArticles(
    #     {
    #         # 发布状态
    #         "status":['Public' ], "subcate":0, "atype":[], "cate":0,
    #         # 第几页
    #         "page":1,
    #         # 每一页展示多少条数据   # 时间倒序排序      # 搜索
    #         "size":3,              "sort":{"TimeDesc"},"search":"",
    #     }
    # )

    # type ListProposalInfo = record {
    #     include_reward_status : vec int32;
    #     before_proposal : opt NeuronId;
    #     limit : nat32;
    #     exclude_topic : vec int32;
    #     include_status : vec int32;
    # };
    # list_proposals : (ListProposalInfo) -> (ListProposalInfoResponse) query;
    # type NeuronId = record { id : nat64 };
    # res = governance.list_proposals(
    #     {
    #         'include_reward_status': [], 
    #         'before_proposal': [],
    #         'limit': 100, 
    #         'exclude_topic': [], 
    #         'include_status': [1]
    #     }
    # )
    # res = user_governance.queryArticles(
    #     {
    #         # 发布状态
    #         "status":{"public"}, "subcate":0, "atype":[{"Article"}], "cate":0,
    #         # 第几页
    #         "page":1,
    #         # 每一页展示多少条数据   # 时间倒序排序      # 搜索
    #         "size":3,              "sort":{"TimeDesc"},"search":"",
    #     }
    # )
    # type ArticleType = 
    # variant {
    #     Article;
    #     Audio;
    #     Photos;
    #     Shortle;
    #     Video;
    # };
    # type QuerySort = 
    # variant {
    #     TimeAsc;
    #     TimeDesc;
    # };
    # type ArticleStatus = 
    # variant {
    #     Delete;
    #     Draft;
    #     Private;
    #     Public;
    #     Subcribe;
    # };
    # type NeuronIdOrSubaccount = variant {
    #     Subaccount : vec nat8;
    #     NeuronId : NeuronId;
    # };
    # type QueryArticleReq = 
    #     record {
    #         atype: opt ArticleType;
    #         cate: nat;
    #         page: nat;
    #         search: text;
    #         size: nat;
    #         sort: QuerySort;
    #         status: opt ArticleStatus;
    #         subcate: nat;
    #     };
    print( 'data=',res[0], 'len=',len(res),'type=',get_type_name(res)  )
    '''
    data = {'total': 11, 'hasmore': False, 'page': 9, 'stat': {'privateCount': 0, 'total': 15, 'draftCount': 0, 'subcribeCount': 4, 'publicCount': 11},'data':[]}
    data = {
        'total': 11,
        'hasmore': True,
        'data': [{
            'id': '0C9YJDSEB7YKBJZZS4NBJ8DC7C',
            'status': {
                'Public': None
            },
            'thumb': 'QmYJNMYynsr3fnsQoFXg7MbQzj3XyW9euSGZofPgcVNyiE',
            'title': 'FKDOM',
            'created': 1702386099668,
            'toped': 0,
            'subcate': 0,
            'atype': {
                'Article': None
            },
            'cate': 0,
            'like': 0,
            'tags': ['fkdom'],
            'view': 0,
            'fromurl': '',
            'unlike': 0,
            'author': Principal(ycaq2-am5es-7ddcs-u5keb-5xawp-k4d3w-tsilc-hd2fk-tiuy4-wopfn-jae),
            'commentTotal': 0,
            'comment': 0,
            'updated': 1702386099668,
            'abstract': 'Mint: { "p": "mora-20", "op": "mint", "tick": "fkdom", "amt": "1" }',
            'allowComment': False,
            'copyright': [],
            'original': True,
            'commentNew': 0
        }, {
            'id': '0C9YCESX6J5TV183NEX5G1DPCJ',
            'status': {
                'Public': None
            },
            'thumb': 'QmeVYdJ4jvV6GcHbE7DdMaNowU2WsnNTibGRkw4oswnWui',
            'title': 'FKDOM',
            'created': 1702386004349,
            'toped': 0,
            'subcate': 0,
            'atype': {
                'Article': None
            },
            'cate': 0,
            'like': 0,
            'tags': [],
            'view': 0,
            'fromurl': '',
            'unlike': 0,
            'author': Principal(ycaq2-am5es-7ddcs-u5keb-5xawp-k4d3w-tsilc-hd2fk-tiuy4-wopfn-jae),
            'commentTotal': 0,
            'comment': 0,
            'updated': 1702386028053,
            'abstract': 'Deploy: { "p": "mora-20", "op": "deploy", "tick": "fkdom", "max": "2100", "lim": "1" } ',
            'allowComment': False,
            'copyright': [],
            'original': True,
            'commentNew': 0
        }],
        'page': 1,
        'stat': {
            'privateCount': 0,
            'total': 15,
            'draftCount': 0,
            'subcribeCount': 4,
            'publicCount': 11
        }
    }
    '''
    # data_list = res[0]
    # print( data_list, len(data_list),get_type_name(data_list)  )
    # for item in data_list:
    #     print('')
    #     print(item,len(item),get_type_name(item))




if __name__ == "__main__":
    # query_canister_ids()
    query_user_articles(user_canister_id='tcaj5-pyaaa-aaaan-qdb4q-cai')
    # query_user_articles(user_canister_id=my_canister_id)




# ic_query_user_articles.py


