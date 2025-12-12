from django.shortcuts import render, redirect, get_object_or_404
from .analysis import perform_analysis
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404
import requests
import datetime
from social_django.utils import load_strategy
from django.db.models.functions import Abs
from django.db.models import F, Func, FloatField


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

            #update user's latest compound score
            request.user.profile.latest_compound = compound
            request.user.profile.save()

            entry.user = request.user
            
            #create playlist
            access_token = gettoken(request.user)
            user_id = getspotifyid(access_token)
            uris = rectracks(entry)
            playlist_id = createplaylist(access_token, user_id, sentiment, entry.title)
            addtracks(playlist_id, uris, access_token, entry)

            #store playlist id for public view
            entry.playlist_id = playlist_id
            entry.save()
            commentform = CommentForm()
            replyform = ReplyForm()
            context = {
            'entry': entry,
            'commentform': commentform,
            'replyform': replyform
            } 
            return render(request, "details.html", context)
    else:
        #else create new form for user to fill
        form = JournalEntryForm()
    return render(request, "create.html", {'form': form})

def logout_user(request):
    logout(request)
    return redirect("home")

def details(request, entry_id):
    entry = get_object_or_404(JournalEntry, pk=entry_id)
    if not entry.public and entry.user!= request.user:
        raise Http404("This journal entry either does not exist or you do not have permission to view it.")
    commentform = CommentForm()
    replyform = ReplyForm()
    context = {
        'entry': entry,
        'commentform': commentform,
        'replyform': replyform
        }    
    return render(request, "details.html", context)

def comment_create(request, entry_id):
    entry = get_object_or_404(JournalEntry, pk=entry_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.user = request.user
            comment.save()
    return redirect("details", entry_id)

def reply_create(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent = comment
            reply.user = request.user
            reply.save()
    return redirect("details", comment.entry.id)

def rectracks(entry):
    #determine valence from compound (-1 to 1 -> 0 to 1)
    valence = (entry.compound+1)/2
    if(entry.compound > 0):
        seeds = "b0233fc7-4a00-4660-af2a-3d13a6c67cf0, 9451b6b2-8746-4d43-abd7-c355ed1e3048, aa803503-0c63-43a3-88c7-7bfb47942567, d2cf3dce-fec7-43ba-8020-25c3ec1700c1, 2868f9f8-7088-4f3e-a104-18a6836ad0e3"
    else:
        seeds = "299da30c-af00-443f-8adb-95345bce4579, 5e2c11cc-3f44-45e7-8262-d868908eb76d, c9bf0016-dbc4-491b-a7b7-981218d2761d, f41dd47c-e6ef-45a1-927d-e8ab4899786e"
    negative_seeds= "cc9cd26c-f25a-403c-8c47-2254b197f77b, 0c3ba19d-9e2a-4941-9f68-52c0abbd6254, d03537c2-84d9-418e-b3ee-b31b24616453"
    #recommend songs using valence score
    url = "https://api.reccobeats.com/v1/track/recommendation"
    headers = {'Accept': 'application/json'}
    payload = {
        "size": 7,
        "seeds": seeds,
        "valence": valence,
        "negativeSeeds": negative_seeds,
        "featureWeight": 5,
        }
    if entry.use_liveness:
        payload["liveness"] = entry.liveness
    if entry.use_popularity:
        payload["popularity"] = entry.popularity
    if entry.use_instrumentalness:
        payload["instrumentalness"] = entry.instrumentalness
    print(payload)
    response = requests.request("GET", url, headers=headers, params=payload)
    print(response.status_code)
    #return a list of spotify uris so we can add tracks to playlist later
    data = response.json()
    hrefs = [track["href"] for track in data["content"]]
    track_ids = [href.split('/')[-1] for href in hrefs]
    uris = [f"spotify:track:{id}" for id in track_ids]
    return uris

def gettoken(user):
    social = user.social_auth.get(provider='spotify')
    token = social.get_access_token(load_strategy())
    return token

def getspotifyid(access_token):
    spotify_user = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {access_token}"}).json()
    return spotify_user["id"]

def createplaylist(access_token, user_id, sentiment, title):
    date = datetime.datetime.now().strftime("%B %d, %Y")
    playlist_name = title
    playlist_desc = f"This playlist weas generated using Listen. Created on {date} with a {sentiment} sentiment."
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "name": playlist_name,
        "description": playlist_desc,
        "public": True
        }
    response = requests.post(url, headers=headers, json=payload)
    #return playlist id to add tracks after
    return response.json()["id"]

def addtracks(playlist_id, tracks, access_token, entry):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"uris": tracks}
    requests.post(url, headers=headers, json=payload)

def discovery(request):
    unsorted_entries = JournalEntry.objects.filter(public=True)
    if request.user.profile.latest_compound:
        latest_compound = request.user.profile.latest_compound
        entries = (unsorted_entries.annotate(distance=Abs(F("compound") - latest_compound)).order_by("distance", "-time_created"))
    else:
        entries = unsorted_entries.order_by("-time_created")
    return render(request, "discovery.html", {'entries': entries})

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('details', comment.entry.id)
    return render(request, 'comment_delete.html', {'comment': comment})

def reply_delete(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id, user=request.user)
    if request.method == 'POST':
        reply.delete()
        return redirect('details', reply.parent.entry.id)
    return render(request, 'reply_delete.html', {'reply': reply})

def entry_delete(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('entries')
    return render(request, 'entry_delete.html', {'entry': entry})

@login_required
def settings(request):
    profile = request.user.profile
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
            form = SettingsForm(instance=profile)
    return render(request, "settings.html", {"form":form})

def open_reply_thread(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    replies = comment.replies.all()
    replyform = ReplyForm()
    context = {
        "comment": comment,
        "replies": replies,
        "replyform": replyform
    }
    return render(request, "reply_thread.html", context)