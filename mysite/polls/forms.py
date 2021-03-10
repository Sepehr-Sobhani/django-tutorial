from django import forms
from django.forms import ModelForm, fields, widgets
from .models import Question


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'pub_date': DateTimeInput()
        }
