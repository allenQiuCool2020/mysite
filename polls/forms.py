from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question_text",
        ]


class ChoicesForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = [
            "choice_text",
        ]