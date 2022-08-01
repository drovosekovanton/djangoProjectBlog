from django.urls import path
from django.contrib.auth import views
from .views import IndexView, AllPostsView, AllBloggersView, PostCreateView, PostDetailView, CommentCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # about this mini blogs
    path('posts/', AllPostsView.as_view(), name='posts'),  # all latest posts from all bloggers
    path('bloggers/', AllBloggersView.as_view(), name='bloggers'),  # all bloggers
    # path('blogger/<int:pk>/', BloggerView.as_view(), name='blogger'),  # info about blogger and his latest posts
    path('<int:pk>/', PostDetailView.as_view(), name='post'),  # certain post with comments
    path('create/', PostCreateView.as_view(), name='create_post'),  # create post
    path('<int:pk>/create/', CommentCreateView.as_view(), name='create_comment'),  # create comment
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
