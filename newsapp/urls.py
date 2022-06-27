from django.urls import path
from .views import NewsList, PostDetail, NewsSearch, NewsCreate, NewsEdit, NewsDelete, CeleryView
# cache decorator
from django.views.decorators.cache import cache_page


app_name = 'newsapp'
urlpatterns = [
    path('', cache_page(30)(NewsList.as_view()), name='news_list'),
    # with cache
    # path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]
