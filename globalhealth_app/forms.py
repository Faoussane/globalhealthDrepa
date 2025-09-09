from django import forms
from .models import QuizSubmission

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        
        for question in questions:
            if question.options.count() > 2:
                # Question à choix multiple
                self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(
                    choices=[(opt.id, opt.text) for opt in question.options.all()],
                    widget=forms.CheckboxSelectMultiple,
                    label=question.text
                )
            else:
                # Question vrai/faux ou choix unique
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=[(opt.id, opt.text) for opt in question.options.all()],
                    widget=forms.RadioSelect,
                    label=question.text
                )