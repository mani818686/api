"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from api_basics import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'article',views.ArticleViewSet,basename='viewset')
urlpatterns = [
    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),
    path('admin/', admin.site.urls),
    path('articles',views.article_list,name='list'),
    path('api/articles',views.ArticleAPIView.as_view(),name='listapi'),
    path("api/articles/<int:pk>",views.ArticleDetail.as_view(), name="detailsapi"),
    path("detail/<int:pk>",views.article_detail, name="details"),
    path('generic/api/<int:id>',views.GenericAPIView.as_view(),name='lista'),
    path('generic/api/<int:id>',views.GenericAPIView.as_view(),name='lista'),
    
]

