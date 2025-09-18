"""Forms for creating and editing notes."""

from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Form for Note model."""

    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your note here...",
                    "rows": 5,
                }
            ),
        }
