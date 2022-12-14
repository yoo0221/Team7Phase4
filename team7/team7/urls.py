"""team7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from main import views as mainview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainview.index, name='index'),
    path('searchCourse/', mainview.courseSearch, name='courseSearch'),
    path('courseDetail/<int:courseid>', mainview.courseDetail, name='courseDetail'),
    path('placeDetail/<int:placeid>', mainview.placeDetail, name='placeDetail'),
    path('placeRegist/', mainview.placeRegist, name='placeRegist'),
    path('courseRegist/', mainview.courseRegist, name='courseRegist'),
    path('courseCommentRegist/<int:courseid>', mainview.courseCommentRegist, name='courseCommentRegist'),
    path('placeCommentRegist/<int:placeid>', mainview.placeCommentRegist, name='placeCommentRegist'),
    path('placeRegSubmit/', mainview.placeRegSubmit, name='placeRegSubmit'),
    path('diaryWrite/', mainview.diaryWrite, name='diaryWrite'),
    path('diaryDetail/<int:diaryid>',mainview.diaryDetail, name='diaryDetail'),
    path('diarySubmit/', mainview.diarySubmit, name='diarySubmit'),
    path('courseRegSubmit/', mainview.courseRegSubmit, name='courseRegSubmit'),
    path('courseSearchbyKey/',mainview.courseSearchbyKey, name='courseSearchbyKey'),
    path('registComplete/',mainview.registComplete, name='registComplete'),
    path('test/', mainview.test, name='test'),
    path('menuRegist/', mainview.menuRegist, name='menuRegist'),
    path('account/', include('accounts.urls'))
]

from django.conf.urls.static import static
from django.conf import settings

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)