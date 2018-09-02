from django.urls.conf import path
from .views import *

# app_name: 해당 파일에서 별칭으로 등록된 url들을 호출할 때 별칭으로 호출해 충돌이 생기지 않도록 설정한다.
#           다른 별칭과 충돌이 일어나지 않도록 파일 자체에 그룹 이름을 지정한다.
# reverse('customlogin:signup)
# {% url 'customlogin:signup' %}
app_name = 'customlogin'

urlpatterns = [
    # 127.0.0.1:8000/login/signup
    path('signup/', signup, name = 'signup'),
    # customlogin:signin
    path('signin/', signin, name = 'signin'),
    path('logout/', auth_logout, name = 'logout')
    ]