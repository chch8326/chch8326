"""Django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from vote.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #URL 등록 시 파이썬 코드에서 URL을 외워서 사용하지 않고 별칭을 이용해서 사용할 수 있도록 name 매개변수에 문자열을 대입한다.
    path('admin/', admin.site.urls),
    path('', index, name = 'index'),
    path('<int:question_id>/', detail, name = 'detail'),
    path('vote/', vote, name = 'vote'),
    path('result/<question_id>/', result, name = 'result'),
    path('registerQuestion/', registerQ, name = 'registerQ'),
    path('registerChoice/', registerC, name = 'registerC'),
    path('deleteQ/<int:question_id>/', deleteQ, name = 'deleteQ'),
    path('deleteC/<int:choice_id>/', deleteC, name = 'deleteC'),
    path('updateQ/<int:question_id>/', updateQ, name = 'updateQ'),
    path('updateC/<int:choice_id>/', updateC, name = 'updateC'),    
    # customlogin 폴더에 있는 urls.py에서 처리할수 있도록 등록 
    path('login/', include('customlogin.urls')),
    # app_name을 social로 대체
    path('auth/', include('social_django.urls', namespace = 'social')),
    path('blog/', include('blog.urls'))
]

# 파일 관리 모듈: Pillow
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
