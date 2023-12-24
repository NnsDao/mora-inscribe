# ic_app/management/my_commands/my_custom_command.py
 
from django.core.management.base import BaseCommand, CommandError
 
class Command(BaseCommand):
    help = 'My custom command'
 
    def add_arguments(self, parser):
        parser.add_argument('some_arg', nargs='+', type=int)
 
    def handle(self, *args, **options):
        # Your command logic here
        pass