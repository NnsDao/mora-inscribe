# my_script_one.py
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'My custom script'
    
    def add_arguments(self, parser):
        parser.add_argument('my_arg', nargs='+', type=int)
        parser.add_argument('--option', action='store_true', dest='my_option')
        parser.add_argument('--option_s', type=str, dest='option_s')
        parser.add_argument('--option_t', type=str)
    
    def handle(self, *args, **options):
        my_arg = options['my_arg']
        my_option = options['my_option']
        option_s = options['option_s']
        option_t = options['option_t']
        # 在这里编写你的脚本逻辑，使用 my_arg 和 my_option 参数和选项
        print(f"My script is running with arguments: {my_arg} and option: {my_option} and option_s: {option_s} and option_t: {option_t}")
        # My script is running with arguments: [1, 2, 3] and option: True
        # python manage.py my_script 1 2 3 --option --option_s=ffff  --option_t=tt
        # My script is running with arguments: [1, 2, 3] and option: True and option_s: ffff and option_t: tt
# python manage.py my_script 1 2 3 --option
# My script is running with arguments: [1, 2, 3] and option: True and option_s: None and option_t: None

# python manage.py runscript my_script --script-args arg1 arg2










