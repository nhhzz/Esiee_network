from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.utils.html import escape
from django.utils.timesince import timesince
from django.template.defaultfilters import linebreaksbr
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from users.models import Follow

@login_required
def posts_list(request):
    filter_follow = request.GET.get("filter")

    if filter_follow == "following":
        followed_users = Follow.objects.filter(
            follower=request.user
        ).values_list("followed", flat=True)

        posts = Post.objects.filter(
            author__in=followed_users
        ).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")

    comment_form = CommentForm()

    return render(request, 'posts/index.html', {
        'posts': posts,
        'comment_form': comment_form,
        'form': PostForm(),
        'filter_follow': filter_follow,
    })



@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "liked": created,
            "count": post.total_likes(),
        })
    return redirect(request.META.get("HTTP_REFERER", reverse("posts_list")))




@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        parent_id = request.POST.get("parent_id")

        if form.is_valid():
            parent = None
            if parent_id:
                parent = Comment.objects.get(id=parent_id)

            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.parent = parent   
            comment.save()

<<<<<<< HEAD
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "id": comment.id,
                    "user": comment.user.username,
                    "created_at": timesince(comment.created_at),
                    "text_html": linebreaksbr(escape(comment.text)),
                })

    return redirect('posts_list')
=======
    return redirect('posts:posts_list')
>>>>>>> 87eedfd77abdbed83a4fcf0ea37b35a83a77d6bd

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user:
        return redirect('posts:posts_list')
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('posts:posts_list')

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('posts:posts_list')

    post.delete()
    return redirect('posts:posts_list')

@login_required
@require_POST
def reply_comment(request, comment_id):
    parent = Comment.objects.get(id=comment_id)
    
    if request.method == "POST":
        text = request.POST.get("reply")
        Comment.objects.create(
            user=request.user,
            post=parent.post,
            parent=parent,
            text=text
        )
    return redirect("posts:posts_list")

@login_required
@require_POST
def create_post(request):
<<<<<<< HEAD
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts_list')

    # If invalid, re-render list with errors instead of silent redirect
    posts = Post.objects.all().order_by("-created_at")
    comment_form = CommentForm()
    return render(request, 'posts/index.html', {
        'posts': posts,
        'comment_form': comment_form,
        'form': form,
    })
=======
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:posts_list')
    else:
        form = PostForm()

    return redirect('posts:posts_list')
>>>>>>> 87eedfd77abdbed83a4fcf0ea37b35a83a77d6bd
