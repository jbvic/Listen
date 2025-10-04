from django.apps import AppConfig
import nltk
from nltk.data import find
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class ListenappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listenapp'

    def ready(self):
        #check if vader files already downloaded
        try:
            find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')

        #initialize sia
        from . import analysis
        analysis.sia = SentimentIntensityAnalyzer()
