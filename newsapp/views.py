# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Author, Category, Post, Comment, PostCategory
from .filters import PostFilter
from .forms import PostForm, ProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, Http404
# Authentication imports
# from django.utils.decorators import method_decorator
# from django.views.generic import TemplateView
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
# mailing
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from project.settings import DEFAULT_FROM_EMAIL
# Celery
from .tasks import hello, printer
# caching
from django.core.cache import cache
import logging
import pytz
from django.utils import timezone


logger = logging.getLogger(__name__)


def set_timezone(request):
    context = {
        'current_time': timezone.localtime(timezone.now()),
        'timezones': pytz.common_timezones
    }
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'default.html', context)


class NewsList(ListView):
    # model name
    model = Post
    # ordering field
    ordering = '-dateCreation'
    # template name
    template_name = 'news_list.html'
    # object list
    context_object_name = 'news_list'
    paginate_by = 10

    # post list generation
    def get_queryset(self):
        queryset = super().get_queryset()
        # current_url = self.request.path
        # different view for news and articles posts
        postType = self.kwargs['postType']
        if postType == 'news':
            self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.NEWS))
        elif postType == 'articles':
            self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.ARTICLE))
        else:
            self.filterset = PostFilter(self.request.GET, queryset.none())
            raise Http404('Page not found')
            # HttpResponseNotFound('Not found')
            # return self.model.objects.none()

        # if current_url.split('/')[1] == 'news':
        #     self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.NEWS))
        # else:
        #     self.filterset = PostFilter(self.request.GET, queryset.filter(categoryType=Post.ARTICLE))
        return self.filterset.qs

    # additional data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # timezone
        curent_time = timezone.now()
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        # adding filtering object
        context['filterset'] = self.filterset
        return context


class NewsSearch(NewsList):
    template_name = 'news_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class PostDetail(DetailView):
    # model name
    model = Post
    # template name
    template_name = 'post.html'
    # object name
    context_object_name = 'post'
    queryset = Post.objects.all()

    # cache
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catType'] = str(self.object.categoryType)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    # custom form
    form_class = PostForm
    # model
    model = Post
    # template
    template_name = 'post_edit.html'
    permission_required = ('newsapp.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context

    def form_valid(self, form):
        # current_url = self.request.path
        post = form.save(commit=False)
        # different categories for news and articles posts
        postType = self.kwargs['postType']
        if postType == 'news':
            post.categoryType = self.model.NEWS
        elif postType == 'articles':
            post.categoryType = self.model.ARTICLE
        self.object = form.save()
        redirectURL = '/' + postType + '/' + str(self.object.id)

        # mailing through html rendering
        # html_content = render_to_string(
        #     'post_created_mail.html',
        #     {
        #         'post': post,
        #         'redirectURL': redirectURL,
        #     }
        # )
        # # mailing list
        # mailing_list = list(set(post.postCategory.all().values_list('subscribers__email', flat=True)))
        # if mailing_list.count(''):
        #   mailing_list.remove('')
        # if len(mailing_list):
        #     msg = EmailMultiAlternatives(
        #         subject=f'{self.object.author.authorUser.username}: {self.object.title} '
        #                 f'{self.object.dateCreation.strftime("%d.%m.%Y")}',
        #         body=post.text,
        #         from_email='sqmax@yandex.ru',
        #         to=mailing_list
        #     )
        #     msg.attach_alternative(html_content, 'text/html')
        #     msg.send()

        # straight way mailing
        # send_mail(
        #     subject=f'{self.object.author.authorUser.username}: {self.object.title} {self.object.dateCreation.strftime("%d.%m.%Y")}',
        #     message=self.object.text,
        #     from_email=DEFAULT_FROM_EMAIL,
        #     recipient_list=['msvp@mail.ru']
        # )
        return redirect(redirectURL)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    # custom form
    form_class = PostForm
    # model
    model = Post
    # template
    template_name = 'post_edit.html'
    permission_required = ('newsapp.change_post',)

    def post(self, request, *args, **kwargs):
        # current_url = self.request.path
        redirectURL = f'/{self.kwargs["postType"]}/{self.kwargs["pk"]}'
        self.success_url = redirectURL

        # for i in current_url.split('/'):
        #     if i == 'edit':
        #         redirectURL = redirectURL[:-1]
        #         break
        #     redirectURL += i+'/'
        super().post(request, *args, **kwargs)
        return redirect(redirectURL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('newsapp.delete_post',)

    def post(self, request, *args, **kwargs):
        # current_url = self.request.path
        redirectURL = f'/{self.kwargs["postType"]}/'
        self.success_url = redirectURL
        # tempURL = ''
        # for i in current_url.split('/'):
        #     if i == 'delete':
        #         redirectURL = tempURL[:-1]
        #         break
        #     else:
        #         tempURL = redirectURL
        #     redirectURL += i + '/'
        return super().post(request, *args, **kwargs)
        # return redirect(redirectURL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context

# Authentication class examples
# class ProtectedView(TemplateView):
#     template_name = 'protected_page.html'
#
#     @method_decorator(login_required):
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


# @method_decorator(login_required, name='dispatch')
# class ProtectedView(TemplateView):
#     template_name = 'protected_page.html'
#
#
# class ProtectedViewM(LoginRequiredMixin, TemplateView):
#     template_name = 'protected_page.html'


class ProfileEdit(LoginRequiredMixin, UpdateView):
    # custom form
    form_class = ProfileForm
    # model
    model = User
    # template
    template_name = 'profile_edit.html'


class CeleryView(View):
    def get(self, request):
        # printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')
