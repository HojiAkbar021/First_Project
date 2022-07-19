from django.urls import path
from apps.posts.views import post_detail, post_update, post_delete, post_search


urlpatterns = [
    path('post/<str:slug>', post_detail, name = "post_detail"),
    path('update/<str:slug>', post_update, name = "post_update"),
    path('delete/<str:slug>', post_delete, name = "post_delete"),
    path('search/', post_search, name = "post_search"),
]