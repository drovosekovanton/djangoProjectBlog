from django.shortcuts import render
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'miniblog/index.html'


class AllBloggersView(generic.ListView):
    pass


class AllPostsView(generic.ListView):
    pass

