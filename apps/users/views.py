from django.shortcuts import render, redirect
from apps.settings.models import Setting
from apps.users.models import User
from django.shortcuts import HttpResponse
from apps.posts.models import Post, FavoritePost, Category, PostImage
from django.contrib.auth import login, authenticate
from django.db import models

# Create your views here.
def register(request):
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_image = request.FILES.get('profile_image')
        slug = request.POST.get('username')
        if password1 == password2:
            try:
                user = User.objects.create(first_name = first_name, last_name = last_name, email = email, phone = phone, username = username, profile_image = profile_image, slug = slug)
                user.set_password(password1)
                user.save()
                return redirect('user_login')
            except:
                return HttpResponse("Неправильные данные")
        else:
            return HttpResponse("Пароли не совпадают")

    context = {
        'setting' : setting,
    }
    return render(request, 'users/register.html', context)

def user_login(request):
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username = username)
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('index')
        except:
            return HttpResponse("Неправильные данные")
    
    context = {
        'setting' : setting,
    }
    return render(request, 'users/login.html', context)

def profile(request, slug):
    post = Post.objects.get(slug = slug)
    setting = Setting.objects.latest('id')
    if request.method == "POST":
        if 'like' in request.POST:
            post = Post.objects.get(slug = slug)
            try:
                FavoritePost.objects.create(user = request.user, post = post)
            except:
                like = FavoritePost.objects.get(user = request.user, post = post)
                like.delete()
        context = {
            'post' : post,
            'setting' : setting,
        }
        return render(request, 'users/profile.html', context)

def profile(request, slug):
    setting = Setting.objects.latest('id')
    user = User.objects.get(slug = slug)
    users = User.objects.all()
    posts = Post.objects.all()
    favorite = FavoritePost.objects.all()
    categories = Category.objects.all()
    counts = 0
    for post1 in posts:
        if post1.user == user:
            counts += 1
    if request.method == "POST":
        if 'create' in request.POST:
            user = User.objects.get(slug = slug)
            title = request.POST.get('title')
            description = request.POST.get('description')
            post_image = request.FILES.get('post_image')
            created = models.DateTimeField(auto_now_add=True)
            category = request.POST.get('category')
            currency = request.POST.get('currency')
            if currency == 'Договорная':
                post = Post.objects.create(user = request.user, title = title, description = description, post_image = post_image, slug = title, created = created, price = 0, currency = currency, category_id = category)
                post_images = request.FILES.getlist('post_images')
                for p_image in post_images:
                    PostImage.objects.create(post_id = post.id, image = p_image)
                return redirect('profile', user.slug)
            else:
                user = User.objects.get(slug = slug)
                title = request.POST.get('title')
                description = request.POST.get('description')
                post_image = request.FILES.get('post_image')
                price = request.POST.get('price')
                created = models.DateTimeField(auto_now_add=True)
                category = request.POST.get('category')
                currency = request.POST.get('currency')
                post = Post.objects.create(user = request.user, title = title, description = description, post_image = post_image, slug = title, created = created, price = price, currency = currency, category_id = category)
                post_images = request.FILES.getlist('post_images')
                for p_image in post_images:
                    PostImage.objects.create(post_id = post.id, image = p_image)
                return redirect('profile', user.slug)
    if request.method == "POST":
        if 'delete' in request.POST:
            user = User.objects.get(slug = slug)
            user.delete()
            return redirect('user_login')
    if request.method == "POST":
        if 'update' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            profile_image = request.FILES.get('profile_image')
            phone = request.POST.get('phone')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            user = User.objects.get(slug = slug)
            if password1 == password2:
                try:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username 
                    user.email = email 
                    user.profile_image = profile_image
                    user.phone = phone 
                    user.slug = username
                    user.set_password(password1)
                    user.save()
                    return redirect('profile', user.slug)   
                except:
                    return HttpResponse("Неправильные данные")
            else:
                return HttpResponse("Пароли не совпадают")

    context = {
        'user' : user,
        'setting' : setting,
        'posts' : posts,
        'favorite' : favorite,
        'users' : users,
        'categories' : categories,
        'counts' : counts,
    }
    return render(request, 'users/profile.html', context)