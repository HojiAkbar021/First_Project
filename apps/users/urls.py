from django.urls import path
from apps.users.views import register, user_login, profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name = "register"),
    path('login/', user_login, name = "user_login"),
    path('accaunt/<str:slug>', profile, name = "profile"),
    path('logout/', LogoutView.as_view(next_page = 'index'), name = "logout"),
]