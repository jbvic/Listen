![Listen_Logo](listenapp/static/logo.png)
# Listen
Listen is a web application that allows users to journal their thoughts and creates a spotify playlist to suit the mood of their journal entry through sentiment analysis. Once a journal entry is saved, a playlist will be generated for the user based on the journal entry’s compound score, allowing the user to listen and save the playlist to their library with a vibe that matches. 
Journal entries can be made public and viewable through a discovery page that is sorted by the user's last compound score. Along with being able to view other people’s journal entries, you can comment on their entries and listen and save their generated spotify playlist to your own spotify library.


# Instalation
1. Clone the repository.
2. Install the requirements using: 
```pip install -r requirements.```
3. Create a Spotify app in the Spotify Developer Dashboard with Web API option.
4. Change client and secret id in settings.py to the one's in your spotify dashboard.
