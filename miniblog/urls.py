from django.urls import path
from django.contrib.auth import views
from .views import IndexView, AllPostsView, AllBloggersView, PostCreate

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('blogs/', AllPostsView.as_view(), name='blogs'),
    path('bloggers/', AllBloggersView.as_view(), name='bloggers'),
    # path('blogger/<pk:user>/', BloggerView.as_view(), name='blogger'),  # info about blogger and some of his posts
    # path('<pk:post>/', PostView.as_view(), name='post'),  # post element with comments
    path('create/', PostCreate.as_view(), name='create_post'),  # create post
    # path('<pk:post>/create/', CommentView.as_view(), name='bloggers'),  # create comment
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
