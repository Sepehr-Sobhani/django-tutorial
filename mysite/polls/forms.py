from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import Choice, Question


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'question_text': forms.Textarea,
            'pub_date': DateTimeInput()
        }
