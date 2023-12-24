#!/usr/bin/env python
# -*- coding:utf-8 -*-





# 最顶级可以创建用户的星球
# https://dashboard.internetcomputer.org/canister/53i5d-faaaa-aaaan-qda6a-cai
# https://github.com/rocklabs-io/ic-py
# https://github.com/tasiafisher/ic_principal.git


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
    principal_a = Principal(b"A")
    print('','principal_a=',principal_a,'principal_a type=',get_type_name(principal_a) ,'principal_a_str=',principal_a.to_str(),'principal_a_str type=',get_type_name(principal_a.to_str() ))
    # self.principal_a = ic.Principal(b"A")
    # self.principal_b = ic.Principal(b"B")



    user_governance = Canister(agent=agent, canister_id=user_canister_id, candid=user_governance_did)
    res = user_governance.getRecoverOwner()
    # getRecoverOwner: () -> (opt principal) query;
    # data= IC0503: Canister fsdio-waaaa-aaaan-qdcea-cai trapped explicitly: assertion failed at main.mo:350.5-350.32 len= 105 type= str
    # data= IC0503: Canister e7nma-ziaaa-aaaan-qdcdq-cai trapped explicitly: assertion failed at main.mo:350.5-350.32 len= 105 type= str

    print( 'data=',res, 'len=',len(res),'type=',get_type_name(res)  )
    
    # isSubscriber: (principal) -> (QueryCommonSubscriber) query;
    # res = user_governance.isSubscriber(principal_a.to_str()) # ValueError: only support string or bytes format

    # print( 'data=',res[0], 'len=',len(res),'type=',get_type_name(res)  )
    



if __name__ == "__main__":
    query_canister_ids()



# ic_is_subscriber.py






# ic_get_user_principal.py



