from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

# 회원가입에 사용할 입력 양식
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # 기존의 기능이 없어지는 것을 막기 위해 상위 클래스의 생성자를 생성한다.
        super().__init__(*args, **kwargs)
        # 객체.fields[키 값]: 해당 폼 클래스에서 설정한 fields, 변수에 입력되는 설정값들을 수정, 읽을 수 있다.
        # 객체.fields[키 값].label: label 태그에 들어갈 문구를 저장한 변수
        self.fields['username'].label = "아이디"
        self.fields['password'].label = "비밀번호"
        self.fields['email'].label = "email"
        self.fields['password_check'].label = "비밀번호 확인"
        
    # 비밀번호 확인
    # 모델클래스와 유사하게 XXXField 클래스의 객체를 변수에 저장해 새로운 input 태그를 생성할 수 있다.
    password_check = forms.CharField(max_length = 200, widget = forms.PasswordInput())
    
    class Meta:
        model = User
        # widgets: 각 변수에 입력 스타일을 설정할 때 사용한다.
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput()
            }
        fields = ['username', 'password', 'email']
        
# 로그인에 사용할 입력양식
class LoginForm(ModelForm):
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput()}
        fields = ['username', 'password']