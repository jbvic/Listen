import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#sia initialized in apps.py, just declared here
sia = None

def perform_analysis(text):
    if sia is None:
        raise RuntimeError("Sentiment intensity analyzer not initialized yet.")
    return sia.polarity_scores(text)