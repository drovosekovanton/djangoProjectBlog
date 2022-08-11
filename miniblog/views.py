from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from rest_framework import viewsets, mixins

from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment


class IndexView(TemplateView):
    """
    Displays page with project description
    """
    template_name = 'miniblog/index.html'


class AllBloggersView(ListView):
    """
    Displays all users ever posted
    """
    model = User
    paginate_by = 5
    template_name = 'miniblog/bloggers_all.html'

    # ordering = ['username']

    def get_queryset(self):
        # bad query, need to rewrite
        return User.objects.filter(post__isnull=False).distinct().order_by('username')


class BloggerView(ListView):
    """
    Displays single blogger detail with paginated list of his post
    """
    model = Post
    template_name = 'miniblog/blogger_detail.html'
    paginate_by = 5

    def get_queryset(self):
        """
        Returns queryset of one's blogger ordered by date posts
        """
        return Post.objects.filter(user=User(pk=self.kwargs['pk'])).order_by('-date_published')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Adds to context blogger object (User)
        """
        context = super(BloggerView, self).get_context_data(**kwargs)
        context['blogger'] = User.objects.get(pk=self.kwargs['pk'])
        return context


class AllPostsView(ListView):
    """
    Paginated display of all post ranged by date
    """
    model = Post
    template_name = 'miniblog/post_all.html'
    paginate_by = 5
    ordering = ['-date_published']


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Displays form to add new post record
    """
    model = Post
    fields = ['post_title', 'post_text']
    template_name_suffix = '_create_form'
    login_url = 'login'
    permission_required = 'miniblog.add_post'
    permission_denied_message = 'You have to be in bloggers group to create posts!'

    def form_valid(self, form):
        """
        Inserts non-editable fields like user and date
        """
        form.instance.user = self.request.user
        form.instance.date_published = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects to newly created post detail page
        """
        return reverse('post', kwargs={'pk': self.object.pk})


class CommentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Displays a form to add a comment to the specific post
    """
    model = Comment
    fields = ['comment_text']
    template_name_suffix = '_create_form'
    login_url = 'login'
    permission_required = 'miniblog.add_comment'

    def get_context_data(self, **kwargs):
        """
        Adds related post to context
        """
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['related_post'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        """
        Inserts non-editable fields like user and date
        """
        form.instance.user = self.request.user
        form.instance.date_published = timezone.now()
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects to specific post with newly added comment
        """
        return reverse('post', kwargs={'pk': self.object.post.pk})


class PostDetailView(DetailView):
    """
    Displays detailed post info with its comments
    """
    model = Post
    template_name = 'miniblog/post_detail.html'

    def get_context_data(self, **kwargs):
        """
        Adds to context related comments sorted by their date in reverse order
        """
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.object.id).order_by('date_published')
        return context


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
