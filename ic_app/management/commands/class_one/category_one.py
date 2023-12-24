from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'My custom command in category 1'

    def handle(self, *args, **options):
        # Your command logic here
        self.stdout.write(self.style.SUCCESS('Hello from my_command1!'))



# from django.core.management.base import BaseCommand, CommandError

# # category_one.py 
# class Command(BaseCommand):
#     help = 'My custom command in category 1'
 
#     def add_arguments(self, parser):
#         # Add any arguments you want here
#         pass

#     def handle(self, *args, **options):
#         # Your command logic here
#         self.stdout.write(self.style.SUCCESS('Hello from my_command1!'))
