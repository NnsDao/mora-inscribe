from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from ic_app.models import op_tick_group as OpTickGroupModel,article_list as ArticleListModel
import json,traceback
from django.core.paginator import Paginator # 导入分页类
from django.core import serializers
from django.forms import model_to_dict   #这个是转字典的，要是不导入这个的话，接口返回json的时候会报错
# Create your views here.


def index(request):
    print('path info is : ', request.path_info)
    print('method is : ', request.method)
    print('querystring is : ', request.GET)
    print(request.GET['a'])
    print(request.GET.getlist('a'))
    print(request.GET.get('c','no have c'))
    print(request.is_ajax())
    print('full path is :', request.get_full_path())
    print('客户端IP is :', request.META['REMOTE_ADDR'])

    # return HttpResponse('test request ok')

    return HttpResponse("请求路径:{}" .format(request.path))

# def index(request):
#     return HttpResponse("Hello World! index")

def initReturnData():
    retData = {'success':False,'code': 0, 'data': {}, 'msg': ''}
    return retData
def hello(request):
    return HttpResponse("Hello World!")

def get_op_tick_list(request):
    retData = initReturnData()
    # retData = {'success':False,'code': 0, 'data': {}, 'msg': '方法错误'}
    if request.method != 'GET' :
        # runLog(content=retData)
        return JsonResponse(retData)
    op_tick_key = request.GET.get('op_tick_group_key','')
    page = request.GET.get('page','1')
    page = int(page)
    size = request.GET.get('size',10)
    size = int(size)
    # if not op_tick_key:
    #     retData['code'] = 2
    #     retData['msg'] = '参数有误'
    #     # runLog(content=retData)
    #     return JsonResponse(retData)
    article_data_list = []
    page_data = []
    json_data = {}
    try:
        article_list_model = OpTickGroupModel.objects.order_by('-created')
        if op_tick_key :
            article_list_model = article_list_model.filter(op_tick_group_key=op_tick_key)
        article_data_list = article_list_model.all()
        paginator = Paginator(article_data_list, size) # 每页有几个数据
        # page_obj = paginator.page(page) # 获取第一页的所有对象
        # page_data = page_obj.object_list 

        # 获取请求的页码。默认为第一页
        # page_number = request.GET.get('page')
        page_data = paginator.get_page(page)
        # json_data=serializers.serialize("json",page_data,ensure_ascii=False)
        retData['success'] = True
        retData['code'] = 200
        retData['msg'] = ''
        # 将数据转换为 JSON 格式
        retData['total_count'] = paginator.count
        # retData['page_range'] = paginator.page_range
        retData['total_pages'] = paginator.num_pages
        retData['current_page'] = page
        retData['size'] = size
        # page是否还有下一页
        retData['has_next'] = page_data.has_next()
        
        # retData['data'] = [{'id': item.id, 'article_id': item.article_id, 'title': item.title} for item in page_data]  # 当前页的数据
        retData['data'] = [model_to_dict(item) for item in page_data]  # 当前页的数据
        # retData['data'] = json_data  # 当前页的数据
        
        
        # retData['total_count'] = paginator.count  
    
        # print('')
        # print('---page_data---',page_data)
        # print('')
        # print('')
        # Object of type Page is not JSON serializable

        # cookieOne = cookieDataOne['cookie_one']
    except Exception as e:
        # print('--e--',e)
        errInfo = traceback.format_exc()
        # print('--errInfo--',user_id,errInfo)
        # runLog(content=errInfo)
        cookieOne = ''
        retData['success'] = False
        retData['code'] = 8
        retData['msg'] = errInfo
    # if not article_data_list :
    #     retData['code'] = 3
    #     retData['msg'] = '获取失败'    
    #     # runLog(content=retData)
    #     return JsonResponse(retData)
    # retData['data'] = json_data
    return JsonResponse(retData)



def get_article_list(request):
    retData = initReturnData()
    # retData = {'success':False,'code': 0, 'data': {}, 'msg': '方法错误'}
    if request.method != 'GET' :
        # runLog(content=retData)
        return JsonResponse(retData)
    article_id = request.GET.get('article_id','')
    canister_id = request.GET.get('canister_id','')
    atype = request.GET.get('atype','')
    
    page = request.GET.get('page','1')
    page = int(page)
    size = request.GET.get('size',10)
    size = int(size)
    # if not op_tick_key:
    #     retData['code'] = 2
    #     retData['msg'] = '参数有误'
    #     # runLog(content=retData)
    #     return JsonResponse(retData)
    article_data_list = []
    page_data = []
    json_data = {}
    try:
        article_list_model = ArticleListModel.objects.order_by('-created')
        if article_id :
            article_list_model = article_list_model.filter(article_id=article_id)
        if canister_id :
            article_list_model = article_list_model.filter(canister_id=canister_id)
        if atype :
            article_list_model = article_list_model.filter(atype=atype)
            
        article_data_list = article_list_model.all()
        paginator = Paginator(article_data_list, size) # 每页有几个数据
        # page_obj = paginator.page(page) # 获取第一页的所有对象
        # page_data = page_obj.object_list 

        # 获取请求的页码。默认为第一页
        # page_number = request.GET.get('page')
        page_data = paginator.get_page(page)
        # json_data=serializers.serialize("json",page_data,ensure_ascii=False)
        retData['success'] = True
        retData['code'] = 200
        retData['msg'] = ''
        # 将数据转换为 JSON 格式
        retData['total_count'] = paginator.count
        # retData['page_range'] = paginator.page_range
        retData['total_pages'] = paginator.num_pages
        retData['current_page'] = page
        retData['size'] = size
        # page是否还有下一页
        retData['has_next'] = page_data.has_next()
        
        # retData['data'] = [{'id': item.id, 'article_id': item.article_id, 'title': item.title} for item in page_data]  # 当前页的数据
        retData['data'] = [model_to_dict(item) for item in page_data]  # 当前页的数据
        # retData['data'] = json_data  # 当前页的数据
        
        
        # retData['total_count'] = paginator.count  
    
        # print('')
        # print('---page_data---',page_data)
        # print('')
        # print('')
        # Object of type Page is not JSON serializable

        # cookieOne = cookieDataOne['cookie_one']
    except Exception as e:
        # print('--e--',e)
        errInfo = traceback.format_exc()
        # print('--errInfo--',user_id,errInfo)
        # runLog(content=errInfo)
        cookieOne = ''
        retData['success'] = False
        retData['code'] = 8
        retData['msg'] = errInfo
    # if not article_data_list :
    #     retData['code'] = 3
    #     retData['msg'] = '获取失败'    
    #     # runLog(content=retData)
    #     return JsonResponse(retData)
    # retData['data'] = json_data
    return JsonResponse(retData)



