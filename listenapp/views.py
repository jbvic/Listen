from django.shortcuts import render, redirect
from .analysis import perform_analysis
from .models import JournalEntry
from .forms import JournalEntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404


# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def listout(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-time_created')
    return render(request, "entries.html", {'entries': entries})

@login_required
def create(request):
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
            entry.user = request.user
            entry.save()
            return render(request, "details.html", {"entry": entry})
    else:
        #else create new form for user to fill
        form = JournalEntryForm()
    return render(request, "create.html", {'form': form})

def logout_user(request):
    logout(request)
    return redirect("home")

def details(request, entry_id):
    try:
        entry = JournalEntry.objects.get(pk=entry_id)
    except JournalEntry.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "details.html", {"entry": entry})