

from django.urls import path
from .views import *
urlpatterns = [
    # path('', post_list, name='post_list'),
    path('', PostListView.as_view(), name='post_list'),
    path('post_create/',post_create, name='post_create'),
    path('post_delete/<int:id>',post_delete,name='post_delete'),
    path('post_update/<int:id>',post_update,name='post_update'),
    path('register_view/',register_view, name='register_view'),
    path('login_view/',login_view, name='login_view'),
    path('logout_view/',logout_view, name='logout_view'),
    path('comment/<int:post_id>/', comment, name='comment'), 
    path('only/<int:id>/',only, name='only'),
]

