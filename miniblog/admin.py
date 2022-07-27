from django.contrib import admin
from django.contrib.auth.models import User
from miniblog.models import BlogUser, Post, Comment


class BloggerInline(admin.TabularInline):
    model = BlogUser
    verbose_name_plural = 'bloggers'


class BloggerAdmin(admin.ModelAdmin):
    inlines = [BloggerInline]


class CommentsInline(admin.TabularInline):
    model = Comment
    verbose_name_plural = 'comments'


admin.site.register(BlogUser, BloggerAdmin)
admin.site.register(Post)
# TODO: tie comments with post somehow
# admin.site.register(Comment)
