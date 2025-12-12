from django import forms
from django.forms import ModelForm
from .models import *
# make a form for the journal entry from a model using modelform

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        #only fields we want to be editable is text field and if entry is public, so only pass in text and public
        fields = ['title', 'text', 'public', 'use_liveness', 'liveness', 'use_popularity', 'popularity', 'use_instrumentalness', 'instrumentalness']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title...'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                "rows": 10,
                'placeholder': "Write your journal entry here... You can write about your day or how you're feeling about something."
            }),
            'public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'use_liveness': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'liveness': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': '0.0',
                'max': '1.0',
                'step': '0.01',
                'type': 'range'
            }),
            'use_popularity': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'popularity': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': '0',
                'max': '100',
                'step': '1',
                'type': 'range'
            }),
            'use_instrumentalness': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'instrumentalness': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': '0.0',
                'max': '1.0',
                'step': '0.01',
                'type': 'range'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control me-2',
                'placeholder': 'Enter a comment...'
                })
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control me-2',
                'placeholder': 'Enter a reply...'
                })
        }

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['text_color', 'font', 'background_color', 'use_display_name']
        widgets = {
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'use_display_name': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }