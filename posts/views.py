from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm

@login_required
def posts_list(request):
    posts = Post.objects.all().order_by("-created_at")
    comment_form = CommentForm()

    return render(request, 'posts/index.html', {
        'posts': posts,
        'comment_form': comment_form,
        'form': PostForm(),
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

    return redirect('posts_list')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user:
        return redirect('posts_list')
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('posts_list')

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('posts_list')

    post.delete()
    return redirect('posts_list')

@login_required
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
    return redirect("posts_list")

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts_list')
    else:
        form = PostForm()

    return redirect('posts_list')
