from django.urls import path
from .views import all_list,detail,post_create,like_post,post_edit,post_delete

app_name='blog'
urlpatterns = [
    path('',all_list,name='all_list'),
    path('create_post',post_create,name='post_create'),
    path('detail/<str:slug>/',detail,name='detail_post'),
    path('detail/<str:slug>/edit', post_edit, name='post_edit'),
    path('<str:slug>/delete', post_delete, name='post_delete'),
    path('like/',like_post,name='like_post'),

    
]
