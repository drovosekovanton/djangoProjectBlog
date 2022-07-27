from django.urls import path
from .views import IndexView, AllPostsView, AllBloggersView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('blogs', AllPostsView.as_view(), name='blogs'),
    path('bloggers', AllBloggersView.as_view(), name='bloggers'),
]
