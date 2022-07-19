from django.shortcuts import render
from apps.settings.models import Setting
from apps.posts.models import Post

# Create your views here.
def index(request):
    setting = Setting.objects.latest('id')
    posts = Post.objects.all().order_by('?')
    pros = Post.objects.filter(status__contains = 'Pro').order_by('?')
    context = {
        'setting' : setting,
        'posts' : posts,
        'pros' : pros,
    }
    return render(request, 'users/index.html', context)