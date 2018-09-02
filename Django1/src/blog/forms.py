from django.forms.models import ModelForm
from .models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['type', 'headline', 'content']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            # 사용자가 글 종류를 선택하지 않았을 때의 값
            self.fields['type'].empty_label = None
            self.fields['type'].label = "글 종류"