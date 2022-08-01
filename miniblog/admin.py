from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from miniblog.models import BlogUser, Post, Comment


class BlogUserInline(admin.StackedInline):
    model = BlogUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (BlogUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Post)

