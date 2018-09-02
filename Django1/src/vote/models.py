from django.db import models
from django.contrib.auth.models import User

# 모델클래스 정의 시 models.py에 있는 Model 클래스를 상속 받는다.
class Question(models.Model):
    # 하나의 유저가 여러개의 Question을 만들 수 있도록 외래키를 설정한다.
    # 글쓴이를 저장하는 외래키
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    # models.CharField(max_length = ): 문자열에 글자 수 제한을 둔다.
    question_text = models.CharField("질문 문구", max_length = 200)
    
    # 날짜와 시간 정보를 저장함
    pub_date = models.DateTimeField("작성일")
    
    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    choice_text = models.CharField("답변",max_length = 100)
    
    # models.IntegerField(): 정수 값을 저장함
    # default = 0: 처음 값은 0부터 시작
    votes = models.IntegerField("투표 수",default = 0)
    
    # models.ForeignKey(): 다른 모델클래스와 연결고리를 만들 때 사용
    # on_delete = models.CASCADE: 연결지은 모델클래스의 객체가 삭제될 경우 하위 항목들도 모두 사라진다. 
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.choice_text
