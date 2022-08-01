from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, BlogUser, Comment
from django.utils import timezone


class IndexView(TemplateView):
    template_name = 'miniblog/index.html'


class AllBloggersView(ListView):
    pass


class AllPostsView(ListView):
    model = Post
    template_name = 'miniblog/post_all.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_text']
    template_name_suffix = '_create_form'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user.bloguser
        form.instance.date_published = timezone.now()
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment_text']
    template_name_suffix = '_create_form'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user.bloguser
        form.instance.date_published = timezone.now()
        form.instance.post = Post.objects.get(self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.post.pk})


class PostDetailView(DetailView):
    model = Post
    template_name = 'miniblog/post_detail.html'

    # override context data
    # def get_context_data(self, *args, **kwargs):
    #     context = super(PostDetailView,
    #                     self).get_context_data(*args, **kwargs)
    #     # add extra field
    #     context["category"] = "MISC"
    #     return context

