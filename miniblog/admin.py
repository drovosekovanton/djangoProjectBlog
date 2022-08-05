from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from miniblog.models import BlogUser, Post, Comment


class BlogUserInline(admin.TabularInline):
    """
    Inlined info of specific user, such as Bio
    """
    model = BlogUser
    can_delete = False
    extra = 1


class CommentInline(admin.TabularInline):
    """
    Inlined comments to the specific post
    """
    model = Comment
    can_delete = True
    extra = 0
    fieldsets = [
        (None, {'fields': ['user', 'date_published', 'comment_text']}),
    ]


class UserAdmin(BaseUserAdmin):
    """
    Default user with inlined Bio
    """
    inlines = [BlogUserInline]


class PostAdmin(admin.ModelAdmin):
    """
    Post record with inlined comments
    """
    inlines = [CommentInline]


# Register new basic user with inlined extra data
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# register post with inlined comments
admin.site.register(Post, PostAdmin)
