from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Author, Category, Post, Comment
# from datetime import datetime


class NewsList(ListView):
    # model name
    model = Post
    # ordering field
    ordering = '-dateCreation'
    # template name
    template_name = 'news_list.html'
    # object list
    context_object_name = 'news_list'

    # additional data
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # adding current date
    #     context['time_now'] = datetime.utcnow()
    #     return context


class PostDetail(DetailView):
    # model name
    model = Post
    # template name
    template_name = 'post.html'
    # object name
    context_object_name = 'post'
