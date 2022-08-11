from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LoginView, LogoutView
from .views import \
    IndexView,\
    AllPostsView,\
    AllBloggersView,\
    PostCreateView, \
    PostDetailView, \
    CommentCreateView, \
    BloggerView, \
    UserViewSet, \
    PostViewSet, \
    CommentViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # about this mini blogs
    path('posts/', AllPostsView.as_view(), name='posts'),  # all latest posts from all bloggers
    path('bloggers/', AllBloggersView.as_view(), name='bloggers'),  # all bloggers
    path('blogger/<int:pk>/', BloggerView.as_view(), name='blogger'),  # info about blogger and his latest posts
    path('<int:pk>/', PostDetailView.as_view(), name='post'),  # certain post with comments
    path('create/', PostCreateView.as_view(), name='create_post'),  # create post
    path('<int:pk>/create/', CommentCreateView.as_view(), name='create_comment'),  # create comment
    path('login/', LoginView.as_view(), name='login'),  # default login view
    path('logout/', LogoutView.as_view(), name='logout'),  # default logout view
    path('api/', include(router.urls)),
]
