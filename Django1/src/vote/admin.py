from django.contrib import admin
from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_dispaly = ('id', 'question_text', 'pub_date')
    
class ChoiceAdmin(admin.ModelAdmin):
    fields = ['choice_text', 'question']
    list_dispaly = ('id', 'choice_text', 'votes', 'question')
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)