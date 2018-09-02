from django.forms.models import ModelForm
from .models import *

# form: html 코드에서 사용할 입력양식(form 태그)을 모델클래스에 맞게 자동으로 만들어주거나 커스텀 입력양식을 만드는 기능을 제공한다.
# class 폼글래스명(ModelForm): 모델클래스에 관한 폼을 정의한다.
# class 폼클래스명(Form): html에서 사옹할 커스텀 폼을 정의한다.

# question_text 값을 입력받을 수 있는 입력양식
class QuestionForm(ModelForm):
    # model: 모델클래스명(해당 폼에 매칭할 모델클래스르르 작성한다.)
    # fields: 해당 모델폼을 통해 클라이언트가 입력할 수 있는 데이터를 명시한다.
    # exclude: 모델크래스의 변수 중 명시한 변수명을 제외한 나머지 변수들을 클라이언트가 작성할 수 있도록 제공한다.
    class Meta:
        # 해당 클래스가 Question 모델클래스와 연동됨을 명시한다.
        model = Question
        exclude = ['pub_date', 'author']

#선택지 문구, 어떤질문의 선택지인지 선택 할수있는 입력양식 만들기        
class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text']