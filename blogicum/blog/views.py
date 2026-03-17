from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post

User = get_user_model()


def index(request):
    current_time = timezone.now()
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=current_time).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'blog/index.html'
    context = {'page_obj': page_obj}
    return render(request, template_name=template, context=context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    author = post.author 
    if not post.is_published and author != request.user:
        raise Http404()
    template = 'blog/detail.html'
    form = CommentForm()
    context = {'form': form, 'post': post, 'comments': comments}
    return render(request, template_name=template, context=context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    current_time = timezone.now()
    posts = Post.objects.filter(is_published=True, pub_date__lte=current_time,
                                category=category)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'blog/category.html'
    context = {'page_obj': page_obj, 'category': category}
    return render(request, template_name=template, context=context)


def profile(request, username):
    template = 'blog/profile.html'
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=author,
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': author, 
        'page_obj': page_obj,
        }
    return render(request, template_name=template, context=context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    template = 'blog/create.html'
    context = {'form': form}
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('blog:profile', request.user.username)
    return render(request, template_name=template, context=context)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = get_object_or_404(Post, pk=post_id)
        new_comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def edit_profile(request):
    user = get_object_or_404(User, username=request.user.username)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.username)
    template = 'blog/user.html'
    context = {'form': form}
    return render(request, template_name=template, context=context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author 
    if author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    template = 'blog/create.html'
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    return render(request, template_name=template, context=context)    


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author 
    if author != request.user:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    template = 'blog/create.html'
    context = {'form': form}
    return render(request, template_name=template, context=context)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    author = comment.author 
    if author != request.user:
        return redirect('blog:post_detail', post_id)    
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    template = 'blog/comment.html'
    context = {'form': form, 'comment': comment}
    return render(request, template_name=template, context=context)
    

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    author = comment.author 
    if author != request.user:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)
    template = 'blog/comment.html'
    context = {'comment': comment}
    return render(request, template_name=template, context=context)
