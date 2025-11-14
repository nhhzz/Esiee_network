from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from .forms import PostForm, CommentForm

@login_required
def posts_list(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm(request.POST or None, request.FILES or None)
    comment_form = CommentForm()

    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts_list')

    return render(request, 'posts/index.html', {
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('posts_list')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('posts_list')
