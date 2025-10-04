from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Journal entry model
#needs text, sentiment, the compound score, and the creation time
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sentiment = models.CharField(blank=True, max_length=10)
    compound = models.FloatField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    #return string representation to make it easier to read on admin
    def __str__(self):
        return f"created on {self.time_created} with {self.sentiment} sentiment"