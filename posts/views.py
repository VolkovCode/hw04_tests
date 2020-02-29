from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Post, Group, User
from .forms import PostForm, EditForm


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'posts/index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts}) 


def new_post(request):
    user = request.user
    form = PostForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            n_post = form.save(commit=False)
            n_post.author = user
            n_post.save()
            return redirect('index')
        return render(request, 'posts/new_post.html', {'form': form})        
    form = PostForm()
    return render(request, 'posts/new_post.html', {'form': form})   


def profile(request, username):
    author = get_object_or_404(User, username = username)
    post_list = Post.objects.filter(author = author).order_by('-pub_date')
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    count = post_list.count
    return render(request, "posts/profile.html", {'count':count, 'author':author, 'page': page, 'paginator': paginator})
   
  
def post_view(request, username, post_id):
    author = get_object_or_404(User, username = username)
    post = Post.objects.get(pk=post_id)
    posts = Post.objects.filter(author = author).order_by('-pub_date')
    count = posts.count
    return render(request, "posts/post.html", {'post':post, 'count':count, 'author':author})


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.user != post.author:
        return redirect(post_view)
    form = PostForm(request.POST)
    if form.is_valid():
        post.text = form.cleaned_data['text']
        post.group = form.cleaned_data['group']
        post.save()
        return redirect(index)
    form = PostForm()
    return render(request, "posts/post_edit.html", {"form": form, 'post':post})   
    #return render(request, "posts/post_new.html", {})




  
