from django.urls import path, include
# from .views import articles, article
# from .views import ArticleList, ArticleDetail
from .views import ArticleViewSet, ArticleDetail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    # 1 and 2 v
    # path('articles/', articles, name='articles'),
    # path('articles/<slug:slug>', article, name='article'),
    # 3-5 v Class View
    # path('articles/', ArticleList.as_view(), name='articles'),
    path('articles/<slug:slug>', ArticleDetail.as_view(), name='article'),
    # 6
    path('', include(router.urls))
]
