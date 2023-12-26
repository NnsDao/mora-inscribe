# my_script.py
from django.core.management.base import BaseCommand, CommandError
from ic_app.ic_controller.ic_query_user_articles import ic_data_statistics,getTime

# python django框架4.2.8版本 多个子目录自定义Command 命令


# 教程  自定义Command
# http://www.manongjc.com/detail/63-cylkqnhutqvbqsx.html
# https://backend.devrank.cn/traffic-information/7295783548307605530
# https://zhuanlan.zhihu.com/p/369082484
# https://blog.csdn.net/lxd_max/article/details/134464829
# https://www.jb51.net/article/236739.htm
# https://blog.csdn.net/uysqoperands/article/details/132934507
# https://www.ycpai.cn/python/R2eTyPfr.html
class Command(BaseCommand):
    help = 'My custom script'
    
    def add_arguments(self, parser):
        # 这个参数必传
        # parser.add_argument('my_arg', nargs='+', type=int)
        parser.add_argument('--option', action='store_true', dest='my_option')
        parser.add_argument('--option_s', type=str, dest='option_s')
        parser.add_argument('--option_t', type=str)
    
    def handle(self, *args, **options):
        my_arg = options['my_arg'] if 'my_arg' in options else ''
        my_option = options['my_option']
        option_s = options['option_s']
        option_t = options['option_t']
        # 在这里编写你的脚本逻辑，使用 my_arg 和 my_option 参数和选项
        print(f"My script is running with arguments: {my_arg} and option: {my_option} and option_s: {option_s} and option_t: {option_t}")
        # My script is running with arguments: [1, 2, 3] and option: True
        # python manage.py ic_query_user_article_list 1 2 3 --option --option_s=ffff  --option_t=tt
        # My script is running with arguments: [1, 2, 3] and option: True and option_s: ffff and option_t: tt
        obj = ic_data_statistics()
        time_total_current = getTime()
        formatted_total_start_time = time_total_current['formatted_time']
        # ret = obj.query_canister_ids()
        ret = obj.thread_pool_data()

        time_total_end_current = getTime()
        formatted_total_end_time = time_total_end_current['formatted_time']
        # forma_ted_total_start_time = time_total_end_current['forma_ted_time']
        # print(ret)
        print('formatted_total_start_time=',formatted_total_start_time,'formatted_total_end_time=',formatted_total_end_time)
        
# python manage.py ic_query_user_article_list 1 2 3 --option
# My script is running with arguments: [1, 2, 3] and option: True and option_s: None and option_t: None











