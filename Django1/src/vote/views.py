from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *

import datetime

# view는 함수 또는 클래스 형태로 구현해야 한다.
# 함수 형태로 구현 시 첫번째 매개변수로 request를 받아야 한다.
# request: 웹 클라이언트의 요청에 대한 정보를 알고 있는 매개변수

# 질문 목록 보기
def index(request):
    list = Question.objects.all()
    return render(request, 'vote/index.html', {'question_list':list})

# 설문지 출력 투표 선택
def detail(request, question_id):
    # 매개변수에 작성한 조건에 따라 모델클래스의 객체 1개를 추출한다.
    # 매개변수 이름은 모델클래스에서 작성한 변수를 사용 가능하다.
    # 내부적으로 id 변수(고유 키)가 추가된다.
    obj = Question.objects.get(id = question_id)
    return render(request, 'vote/detail.html', {'question':obj})

# 투표 처리
def vote(request):
    # request.method == 'GET'/'POST': 클라이언트 요청이 GET 방식인지 POST 방식인지 저장하는 변수
    if request.method == 'POST':
        
        # request.POST.get('name값'): POST 방식으로 들어온 데이터중 choice 데이터를 추출한다.
        # get 함수가 반환하는 값은 전부 문자열이다.
        id = request.POST.get('choice')
        
        # pk: Choice 객체의 id 변수와 동일
        obj = get_object_or_404(Choice, pk = id)
        obj.votes += 1
        
        # 객체의 변경 사항을 데이터베이스에 저장
        obj.save()
        
        # HttpResponseRedirect 클래스: 클라이언트에게 html 문서를 전달하지 않고 URL 주소를 전달하고 
        #                            웹 클라이언트는 받은 URL주소로 웹서버에 재요청한다.
        # reverse 함수 : URL의 별칭(name)을 이용해 URL 주소를 찾는 함수이다.
        return HttpResponseRedirect(reverse('result', args = (obj.question.id,)))
    
# 투표 결과 보기
def result(request, question_id):
    obj = get_object_or_404(Question, pk = question_id)
    return render(request, 'vote/result.html', {'obj':obj})
        
# 사용자가 질문 등록
@login_required
def registerQ(request):
    # 하나의 뷰 함수는 사용자가 GET/POST 요청할 때를 구분지어서 작업한다.
    if request.method == 'GET':
        # QuestionForm 객체 생성(비어 있음): 사용자로부터 입력받을 변수값을 html 문서에서 처리할 수 있도록 html 코드로 변환 가능
        # 객체를 생성한 경우 input 태그에 값이 비어있는 상태로 사용자에게 전달한다.
        # register 함수의 경우 새로운 객체를 만들기 때문에 빈 객체(form = QuestionForm())를 만든다.
        form = QuestionForm()
        return render(request, 'vote/registerQ.html', {'form':form})
    
    elif request.method =='POST':
        # request 안에 있는 POST 데이터를 통해 객체 생성
        # 폼 객체 생성시 사용자가 입력한 데이터를 각 폼 변수에 대입한다. 즉, 사용자 데이터를 기반으로 객체를 생성한다.
        form = QuestionForm(request.POST)
        
        # if form.is_valid(): 해당 폼에 입력한 값들이 에러가  없는지, 유효한 값인지 확인해준다.
        #                     객체의 특정 데이터들을 꺼낼 수 있다.
        if form.is_valid():
            # 해당 폼에 입력값들로 모델클래스 객체를 생성 및 데이터베이스에 저장한다.
            # form.save() -> 컴파일 에러: form은 question_text의 값만 들어 있는 상태이므로 바로 세이브를 할 경우
            #                         pub_date의 값이 비어있는 상태로 데이터베이스에 저장이 된다.
            # commit = False: 모델클래스의 객체를 생성만 하고 데아터베이스에 저장을 하지 않는다.
            obj = form.save(commit = False)
            
            # pub_date 값 수정 및 현재 시간을 대입
            obj.pub_date = datetime.datetime.now()
            
            #글쓴이 등록
            obj.author = request.user
                        
            # Question 객체를 데이터베이스에 저장한다.
            obj.save()
            return HttpResponseRedirect(reverse('detail', args = (obj.id,)))
        
# 사용자가 선택지 등록
@login_required
def registerC(request):
    if request.method == 'GET':
        # register 함수의 경우 새로운 객체를 만들기 때문에 빈 객체(form = ChoiceForm())를 만든다.
        form = ChoiceForm()
        return render(request, 'vote/registerC.html', {'form':form})
    
    elif request.method == 'POST':
        form = ChoiceForm(request.POST)
        
        if form.is_valid():
            if request.user == form.cleaned_data['question'].author:
                obj = form.save()
                return HttpResponseRedirect(reverse('detail', args = (obj.question.id,)))
            
            else:
                return render(request, 'vote/registerC.html', {'form':form, 'error':"현재 로그인된 유저의 글이 아닙니다."})
        
# 사용자가 질문 삭제
@login_required
def deleteQ(request, question_id):
    # get_object_or_404: 객체를 찾을 때 사용한다.
    # pk는 id와 동일
    obj = get_object_or_404(Question, pk = question_id)
    
    # 해당 객체를 데이터베이스에서 제거
    obj.delete()
    return HttpResponseRedirect(reverse('index'))

# 사용자가 선택지 삭제
@login_required
def deleteC(request, choice_id):
    obj = get_object_or_404(Choice, pk = choice_id)
    question_id = obj.question.id
    obj.delete()
    return HttpResponseRedirect(reverse('detail', args = (question_id,)))

# 사용자가 질문 수정
@login_required
def updateQ(request, question_id):
    obj = get_object_or_404(Question, pk = question_id)
    
    if request.method == 'GET':
        # register 함수의 경우 빈 객체를 줬지만 update 함수의 경우 기존에 있던 객체를 수정하고 그 값을 다시 받아야하기 때문에 instance를 사용해야 한다.
        # instance: 이미 생성된 모델클래스의 객체를 넣어야 한다.
        #           해당하는 객체에 저장되 있는 데이터들을 뽑아내서 form에 그 객체의 값들을 입력해준다.
        form = QuestionForm(instance = obj)
        return render(request, 'vote/updateQ.html', {'form':form})
    
    elif request.method == 'POST':
        # 이미 생성된 Question 객체의 변수 값들을 클라이언트가 작성한 내용으로 덮어 씌운다.
        form = QuestionForm(request.POST, instance = obj)
        
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(reverse('detail', args = (question.id,)))
        
# 사용자가 선택지 수정
@login_required
def updateC(request, choice_id):
    obj = get_object_or_404(Choice, pk = choice_id)
    
    if request.method == 'GET':
        form = ChoiceForm(instance = obj)
        return render(request, 'vote/updateC.html', {'data':form})
    
    elif request.method == 'POST':
        form = ChoiceForm(request.POST, instance = obj)
        
        if form.is_valid():
            choice = form.save()
            return HttpResponseRedirect(reverse('detail', args = (choice.question.id,)))
        
        # 사용자의 입력이 유효하지 않은 데이터인 경우 다시 html 문서를 전달하면서 특정변수에 에러 문구를 대입한다.
        else:
            return render(request, 'vote/updateC.html', {'data':form, 'error':"유효하지 않은 입력입니다."})