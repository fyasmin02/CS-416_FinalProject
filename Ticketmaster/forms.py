from django import forms
from .models import NoteHistory

#Step 1.2
class NoteForm(forms.ModelForm):
    class Meta:
        model = NoteHistory
        fields = '__all__'