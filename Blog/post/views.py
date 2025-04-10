from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.views.generic import *
from django.views.generic import *
# from django.contrib.auth.mixins import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Comment, Post

# Create your views here.

# @login_required
# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'post/post_list.html', {'posts': posts})

class PostListView( ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'



@login_required
def post_create(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    print(categories)
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        tag_ids = request.POST.getlist('tags')
        image = request.FILES.get('image')
        print(image, 'img')

        category = Category.objects.get(id=category_id)
        post = Post.objects.create(
            title=title, content=content, image=image, category=category)

        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        return redirect('post_list')

    return render(request, 'post/post_create.html', {'categories': categories, 'tags': tags})

@login_required
def post_delete(request,id):
    get_object_or_404(Post,id=id).delete()
    return redirect('post_list')

@login_required
def post_update(request, id):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    post = get_object_or_404(Post, id=id)
    if request.user  != post.user:
        return HttpResponse('this is not your post')
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.category = Category.objects.get(id=request.POST['category'])
        if 'image' in request.FILES:
            post.image = request.FILES['image']

        post.tags.clear()
        tag_ids = request.POST.getlist('tags')
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        post.save()
        return redirect('post_list')
    return render(request, 'post/post_update.html', {'categories':categories, 'tags':tags, 'post':post})

def register_view(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'user already taken or exists ')
            return redirect('register')
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()
        messages.success(request, 'account createed successfully  ')
        return redirect('login_view')
    return render(request, 'user/register_view.html', )


def login_view(request):
    if request.method == "POST":
    
        username = request.POST['username']
        password = request.POST['password']
        # **credentials
        user = authenticate(request, username=username, password=password)
        if user :
            login(request,user)
            messages.success(request, 'login successfully  ')
            return redirect('post_list')
        else:
            messages.error(request, ' invalid credentials ')
            return redirect('login_view')
              
    return render(request, 'user/login.html', )

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, ' logout successfully ')
    return redirect('login_view')
    
    
# mvt orm middlware django thread multi ya single ans asynchronus django , sallary , session , transaction , token , what is class base. rnd
    
# comment functinality , add user multiple comment add  

# def post_detail(request,id):
#     post = get_object_or_404(post, id=id)
#     print(post)
#     return render(request, 'post/post_detail.html', {'post': post})



@login_required  # Restrict access to logged-in users
def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Get the specific post
    comments = Comment.objects.filter(post=post).order_by('-id')  # Show latest comments first

    if request.method == "POST":
        text = request.POST.get('text')

        # Create comment using the logged-in user
        Comment.objects.create(user=request.user, text=text, post=post)

        # Redirect to the same page to clear the form and show the new comment
        return redirect("comment", post_id=post.id)

    return render(request, 'post/comment.html', {'post': post, 'comments': comments})

def only(request, id):
    onl = get_object_or_404(Post, id=id)  
    return render(request, 'post/only.html', {'only': onl})

