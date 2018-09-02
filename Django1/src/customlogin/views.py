from django.shortcuts import render
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

# 회원 가입
def signup(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'user/signup.html', {'form':form})
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        
        # form.is_valid(): 폼 안의 데이터들을 추출하고, UserForm을 기준으로 아이디가 중복되는지, 패스워드가 형식이 지켜졌는지 등을 확인할 수 있다.
        if form.is_valid():
            # form.cleaned_data[키 값]으로 해당 이름으로 저장된 값을 추출할 수 있다.
            # 패스워드와 패스워드 체크가 동일한 값인지 확인
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
                # 회원 생성
                new_user = User.objects.create_user(form.cleaned_data['username'],
                                                    form.cleaned_data['email'],
                                                    form.cleaned_data['password'])
                
                # login(request, user 객체): 해당요청을 가진 클라이언트가 user 객체로 로그인하는 작업을 할 수 있다.
                login(request, new_user)
                return HttpResponseRedirect(reverse('index'))
            
            # 패스워드와 패스워드 체크가 같지 않은 경우
            else:
                return render(request, 'user/signup.html', {'form':form, 'error':"비밀번호가 같지 않습니다."})
            
        # 유효하지 않은 값이 입력된 경우
        else:
            return render(request, 'user/signup.html', {'form':form, 'error':"유효하지 않은 값입니다."})
        
# 로그인
def signin(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/signin.html', {'form':form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        # 사용자가 form을 이용해 작성한 데이터를 가지고 객체를 찾아야 한다.
        id = request.POST.get('username')
        pw = request.POST.get('password')
        
        # authenticate(username, password): User 모델클래스에 해당 아이디와 패스워드를 가진 객체를 찾아 반환한다.
        #                                   단, 객체가 없는 경우 None을 반환한다.
        obj = authenticate(username = id, password = pw)
        
        if obj is not None:
            login(request, obj)
            return HttpResponseRedirect(reverse('index'))
        
        else:
            return render(request, 'user/signin.html', {'form':form, 'error':"아이디 또는 비밀번호가 틀렸습니다."})
        
# 로그아웃
def auth_logout(request):
    # logout(request): 로그아웃을 할 수 있도록 만들어준다.
    logout(request)
    return HttpResponseRedirect(reverse('index'))