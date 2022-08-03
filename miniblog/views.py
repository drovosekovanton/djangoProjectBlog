from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, BlogUser, Comment
from django.contrib.auth.models import User
from django.utils import timezone


class IndexView(TemplateView):
    template_name = 'miniblog/index.html'


class AllBloggersView(ListView):
    model = User
    paginate_by = 5
    template_name = 'miniblog/bloggers_all.html'
    ordering = ['username']


class BloggerView(ListView):
    """
        display single blogger detail with paginated list of his post
    """
    model = Post
    template_name = 'miniblog/blogger_detail.html'
    paginate_by = 5

    # or should we use SingleObjectMixin, like in documentation?
    # https://docs.djangoproject.com/en/4.0/topics/class-based-views/mixins/#using-singleobjectmixin-with-listview

    def get_queryset(self):
        """
        Returns queryset of one's blogger posts
        :return: QuerySet of Post
        """
        return Post.objects.filter(user=User(pk=self.kwargs['pk']))

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Add to context blogger object (User)
        :return: modified context
        """
        context = super(BloggerView, self).get_context_data(**kwargs)
        context['blogger'] = User.objects.get(pk=self.kwargs['pk'])
        return context


class AllPostsView(ListView):
    model = Post
    template_name = 'miniblog/post_all.html'
    paginate_by = 5
    ordering = ['-date_published']


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_title', 'post_text']
    template_name_suffix = '_create_form'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date_published = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment_text']
    template_name_suffix = '_create_form'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['related_post'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date_published = timezone.now()
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.post.pk})


class PostDetailView(DetailView):
    model = Post
    template_name = 'miniblog/post_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context['comments'] = Comment.objects.filter(post_id=self.object.id)
    #     return context
