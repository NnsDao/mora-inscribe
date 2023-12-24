
from django.urls import path
from . import views

app_name = "ic_app"
urlpatterns = [
    path('index/', views.index, name='index'),
    path('hello/', views.hello, name='hello'),
    path('get_op_tick_list', views.get_op_tick_list, name='get_op_tick_list'),
    path('get_article_list', views.get_article_list, name='get_article_list'),
    # path('get_user_notes', views.get_user_notes, name='get_user_notes'),

]


