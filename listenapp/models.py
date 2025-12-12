from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Journal entry model
#needs text, sentiment, the compound score, and the creation time
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    text = models.TextField()
    sentiment = models.CharField(blank=True, max_length=10)
    compound = models.FloatField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    playlist_id = models.CharField(max_length=100, blank=True, null=True)
    public = models.BooleanField(default=False)
    liveness = models.FloatField(blank=True, null=True)
    use_liveness = models.BooleanField(default=False)
    popularity = models.IntegerField(blank=True, null=True)
    use_popularity = models.BooleanField(default=False)
    instrumentalness = models.FloatField(blank = True, null=True)
    use_instrumentalness = models.BooleanField(default=False)
    #return string representation to make it easier to read on admin
    def __str__(self):
        return f"created on {self.time_created} with {self.sentiment} sentiment"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="comments")
    time_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)
    class Meta:
        ordering = ['-time_created']

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    time_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)
    class Meta:
        ordering = ['time_created']

FONTS = [
    ("Segoe UI", "Segoe UI"),
    ("Arial", "Arial"),
    ("Verdana", "Verdana"),
    ("Helvetica Neue", "Helvetica Neue"),
    ("Sans-serif", "Sans-serif"),
    ("Monospace", "Monospace"),
    ("Open Sans", "Open Sans"),
    ("Helvetica", "Helvetica"),
    ("Georgia", "Georgia"),
    ("Font Awesome", "Font Awesome")
    ]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    latest_compound = models.FloatField(null=True, blank=True)
    profile_pic_url = models.URLField(blank=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    use_display_name = models.BooleanField(default=False)
    #text_size = models.CharField(max_length=10, choices=SIZES, default="16px")
    text_color = models.CharField(max_length=20, default="#000000")
    font = models.CharField(max_length=50, choices=FONTS, default="Segoe UI")
    background_color = models.CharField(max_length=20, default="#ffffff")

    @property
    def name(self):
        if self.use_display_name and self.display_name:
            return self.display_name
        return self.user.username