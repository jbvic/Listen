from django.forms import ModelForm
from .models import JournalEntry
# make a form for the journal entry from a model using modelform

class JournalEntryForm(ModelForm):
    class Meta:
        model = JournalEntry
        #only field we want to be editable is text field, so only pass in text field
        fields = ['text']