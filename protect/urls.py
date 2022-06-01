from django.urls import path
from .views import IndexView, subscribe_me


urlpatterns = [
    path('', IndexView.as_view()),
    path('subscribe/', subscribe_me, name='subscribe'),
]
