from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "post_type", "created_at")
    list_filter = ("post_type", "author", "created_at")
    search_fields = ("title", "content")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.image.url)
        return "-"
    image_tag.short_description = "Image"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "parent", "commentContent", "created_at")
    list_filter = ("user", "post", "created_at")
    search_fields = ("user__username", "text", "post__title")

    def commentContent(self, obj):
        return obj.text[:20] + ("..." if len(obj.text) > 20 else "")
    commentContent.short_description = "Comment content"
