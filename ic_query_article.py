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
        print('')
        print('')
        print('------------------------------query_user_articles----------------------------')
        print('Index: {}, Value: {}'.format(index, value))
        query_user_articles(user_canister_id=value)
def query_user_articles(user_canister_id = ''):
    ''' 根据用户-分页返回文章-不同的页数据可能重复 '''
    # Index: 10311, Value: ecj4r-myaaa-aaaan-qja5q-cai

    user_governance = Canister(agent=agent, canister_id=user_canister_id, candid=user_governance_did)
    # 文章列表
    # https://mora.app/planet/gkhdz-7yaaa-aaaan-qi2ra-cai
    # 单个文章
    # https://mora.app/planet/gkhdz-7yaaa-aaaan-qi2ra-cai/0CNTQ850TR0E163DC3YW4J6JK3
    # 0CNTQ850TR0E163DC3YW4J6JK3 是这个用户的一篇文章的id
    res = user_governance.queryArticle('0CNTQ850TR0E163DC3YW4J6JK3')
    # queryArticle: (text) -> (QueryDetailResp) query;

    # type QueryDetailResp
    # variant {
    #     Err: text;
    #     Ok: record {
    #             article: QueryArticle;
    #             content: text;
    #         };
    # };

    # type QueryArticle = 
    # record {
    #     abstract: text;
    #     allowComment: bool;
    #     atype: ArticleType;
    #     author: principal;
    #     cate: nat;
    #     comment: nat;
    #     commentNew: nat;
    #     commentTotal: nat;
    #     copyright: opt text;
    #     created: int;
    #     fromurl: text;
    #     id: text;
    #     like: nat;
    #     original: bool;
    #     status: ArticleStatus;
    #     subcate: nat;
    #     tags: vec text;
    #     thumb: text;
    #     title: text;
    #     toped: int;
    #     unlike: nat;
    #     updated: int;
    #     view: nat64;
    # };
    # type ArticleType = 
    # variant {
    #     Article;
    #     Audio;
    #     Photos;
    #     Shortle;
    #     Video;
    # };
    # data= [{'Err': 'article not exist!'}] len= 1 type= list
    # data = [{'Ok': {'content': '<p>Mint: { "p": "mora-20", "op": "mint", "tick": "ddz", "amt": "1000" }</p>', 'article': {'id': '0CNTQ850TR0E163DC3YW4J6JK3', 'status': {'Public': None}, 'thumb': 'QmWHbJG7Vpy3YGGToCq4Gv2twhja1TX9tEeAj8UPPccW9J', 'title': 'ICLANDLORD', 'created': 1702794262020, 'toped': 0, 'subcate': 0, 'atype': {'Article': None}, 'cate': 0, 'like': 0, 'tags': ['$DDZ'], 'view': 0, 'fromurl': '', 'unlike': 0, 'author': Principal(fsxzs-hinfo-yi3et-va3a7-u6htl-4ubvz-37tui-w37pn-ozd47-4noa2-dqe), 'commentTotal': 0, 'comment': 0, 'updated': 1702794262020, 'abstract': 'Mint: { "p": "mora-20", "op": "mint", "tick": "ddz", "amt": "1000" }', 'allowComment': False, 'copyright': [], 'original': True, 'commentNew': 0}}}]
    print( 'data=',res, 'len=',len(res),'type=',get_type_name(res)  )
    


if __name__ == "__main__":
    # query_canister_ids()
    query_user_articles(user_canister_id=my_canister_id)
    



# ic_query_article.py



