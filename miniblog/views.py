from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, BlogUser
from django.utils import timezone


class IndexView(generic.TemplateView):
    template_name = 'miniblog/index.html'


class AllBloggersView(generic.ListView):
    pass


class AllPostsView(generic.ListView):
    model = Post
    template_name = 'miniblog/post_all.html'


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['post_text']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.user = self.request.user.bloguser
        form.instance.date_published = timezone.now()
        return super().form_valid(form)
