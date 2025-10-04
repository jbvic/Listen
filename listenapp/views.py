from django.shortcuts import render, redirect
from .analysis import perform_analysis
from .models import JournalEntry
from .forms import JournalEntryForm

# Create your views here.


def home(request):
    #check if post, if post perform analysis and save entry
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            #if form is valid, create entry with save, but DO NOT commit so we can perform analysis before saving to database
            entry = form.save(commit=False)
            #perform sentiment analsysis to get scores
            scores = perform_analysis(entry.text)
            #get compound score
            compound = scores['compound']

            #if compound score >=0.05 = positive, <=-0.05 = negative, else = neutral
            if compound >= 0.05:
                sentiment = "positive"
            elif compound <= -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            #set the entry fields with analysis results, then save
            entry.sentiment = sentiment
            entry.compound = compound
            entry.save()
            return redirect("home")
    else:
        #else create new form for user to fill
        form = JournalEntryForm()
    
    entries = JournalEntry.objects.all().order_by('-time_created')
    return render(request, "home.html", {'form': form, 'entries': entries})