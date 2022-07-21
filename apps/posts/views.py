from django.db import models
from django.shortcuts import render, redirect
from apps.categories.models import Category
from apps.posts.models import Post, PostImage, FavoritePost
from apps.settings.models import Setting
from django.db.models import Q
# def post_detail(request, id):
#     post = Post.objects.get(id = id)
#     posts = Post.objects.all().order_by('?')
#     setting = Setting.objects.latest('id')
#     post1 = PostImage.objects.all()
#     if request.method == "POST":
#         post = Post.objects.get(id = id)
#         if post.valid == True:
#             post.valid = False 
#             post.save()
#         if post.valid == False:
#             post.valid = True 
#             post.save()
#         return redirect('profile', request.user.id)
#     context = {
#         'setting' : setting,
#         'post' : post,
#         'posts' : posts,
#         'post1' : post1,
#     }
#     return render(request, 'posts/single.html', context)


# def post_delete(request, id):
#     setting = Setting.objects.latest('id')
#     post = Post.objects.get(id = id)
#     if request.method == 'POST':
#         post = Post.objects.get(id = id)
#         post.delete()
#         return redirect('index')
#     context = {
#         'setting' : setting,
#         'post' : post,
#     }
#     return render(request, 'posts/post_delete.html', context)

# def post_update(request, id):
#     setting = Setting.objects.latest('id')
#     categories = Category.objects.all()
#     post = Post.objects.get(id = id)
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         post_image = request.FILES.get('post_image')
#         price = request.POST.get('price')
#         category = request.POST.get('category')
#         currency = request.POST.get('currency')
#         post = Post.objects.get(id = id)
#         post.title = title
#         post.description = description
#         post.post_image = post_image
#         post.category_id = category
#         post.currency = currency
#         post.price = price
#         post.save()
#         return redirect('post_detail', post.id)
#     context = {
#         'setting' : setting,
#         'categories' : categories,
#         'post' : post,
#     }
#     return render(request, 'posts/post_update.html', context)

def post_update(request, slug):
    setting = Setting.objects.latest('id')
    categories = Category.objects.all()
    post = Post.objects.get(slug = slug)
    if request.method == 'POST':
        currency = request.POST.get('currency')
        title = request.POST.get('title')
        description = request.POST.get('description')
        post_image = request.FILES.get('post_image')
        price = request.POST.get('price')
        category = request.POST.get('category')
        post_images = request.FILES.getlist('post_images')
        for p_image in post_images:
            PostImage.objects.create(post_id = post.id, image = p_image)
        post = Post.objects.get(slug = slug)
        post.title = title
        post.description = description
        post.post_image = post_image
        post.category_id = category
        post.currency = currency
        post.price = price
        post.slug = title
        post.post_images = post_images
        post.save()
        return redirect('post_detail', post.slug)
    context = {
        'setting' : setting,
        'categories' : categories,
        'post' : post,
    }
    return render(request, 'posts/post_update.html', context)


def post_delete(request, slug):
    setting = Setting.objects.latest('id')
    post = Post.objects.get(slug = slug)
    if request.method == 'POST':
        post = Post.objects.get(slug = slug)
        post.delete()
        return redirect('profile', request.user.slug)
    context = {
        'setting' : setting,
        'post' : post,
    }
    return render(request, 'posts/post_delete.html', context)

def post_search(request):
    posts = Post.objects.all()
    setting = Setting.objects.latest('id')
    qury_object = request.GET.get('key')
    if qury_object == "":
        posts = Post.objects.all()
        return redirect('index')
    if qury_object:
        posts = Post.objects.filter(Q(title__icontains = qury_object) | Q(description__icontains = qury_object))
    context = {
        'setting' : setting,
        'posts' : posts,
        'qury_object' : qury_object
    }
    return render(request, 'posts/search.html', context)

def post_detail(request, slug):
    post = Post.objects.get(slug = slug)
    posts = Post.objects.all()
    images = PostImage.objects.all()
    setting = Setting.objects.latest('id')
    random_posts = Post.objects.all().order_by('?')
    if request.method == "POST":
        if 'valid' in request.POST:
            post = Post.objects.get(slug = slug)
            if post.valid == True:
                post.valid = False
                post.save()
                return redirect('profile', request.user.slug)
            else:
                post.valid = True
                post.save()
                return redirect('profile', request.user.slug)
        if request.method == "POST":
            if 'like' in request.POST:
                try:
                    like = FavoritePost.objects.get(user=request.user, post = post)
                    like.delete()
                except:
                    FavoritePost.objects.create(user = request.user, post = post)
    context = {
        'setting' : setting,
        'post' : post,
        'posts' : posts,
        'random_posts' : random_posts,
        'images' : images,
    }
    return render(request, 'posts/single.html', context)
