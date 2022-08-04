from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from miniblog.models import BlogUser, Post, Comment


class BlogUserInline(admin.TabularInline):
    model = BlogUser
    can_delete = False
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    can_delete = True
    extra = 0
    fieldsets = [
        (None, {'fields': ['user', 'date_published', 'comment_text']}),
    ]


class UserAdmin(BaseUserAdmin):
    inlines = [BlogUserInline]


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


# Basic User with inlined extra data
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Post inlined with comments
admin.site.register(Post, PostAdmin)
