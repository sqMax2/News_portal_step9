# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Author, Category, Post, Comment
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    # model name
    model = Post
    # ordering field
    ordering = '-dateCreation'
    # template name
    template_name = 'news_list.html'
    # object list
    context_object_name = 'news_list'
    paginate_by = 3

    # post list generation
    def get_queryset(self):
        queryset = super().get_queryset()
        current_url = self.request.path
        # different view for news and articles posts
        if current_url.split('/')[1] == 'news':
            self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.NEWS))
        else:
            self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.ARTICLE))
        return self.filterset.qs

    # additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # adding filtering object
        context['filterset'] = self.filterset
        return context


class NewsSearch(NewsList):
    template_name = 'news_search.html'


class PostDetail(DetailView):
    # model name
    model = Post
    # template name
    template_name = 'post.html'
    # object name
    context_object_name = 'post'


class NewsCreate(CreateView):
    # custom form
    form_class = PostForm
    # model
    model = Post
    # template
    template_name = 'post_edit.html'

    def form_valid(self, form):
        current_url = self.request.path
        post = form.save(commit=False)
        # different categories for news and articles posts
        if current_url.split('/')[1] == 'news':
            post.categoryType = self.model.NEWS
        else:
            post.categoryType = self.model.ARTICLE
        return super().form_valid(form)


class NewsEdit(UpdateView):
    # custom form
    form_class = PostForm
    # model
    model = Post
    # template
    template_name = 'post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
