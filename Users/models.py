from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import datetime
# Create your models here.

def upload_to_Profile(instance, filename):
    return 'profile/{filename}'.format(filename=filename)

def upload_to_Topic(instance, filename):
    return 'topics/{filename}'.format(filename=filename)

def upload_to_Thread(instance, filename):
    return 'threads/{filename}'.format(filename=filename)

class Topic(models.Model):
    title = models.TextField(default="")
    media = models.FileField(upload_to=upload_to_Topic, max_length=256, blank=True, default='topics/default.jpg')

class Profile(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    likesGiven = models.PositiveIntegerField(default=0)
    organisation = models.TextField(default="")

    def __str__(self):
        return "user_" + str(self.pk) + "_" + str(self.userID.username)


class Thread(models.Model):
    title = models.TextField(default="")
    postedAt = models.DateTimeField(default=datetime.datetime.now())
    content = models.TextField(default="")
    upvotes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    topicID = models.ForeignKey(Topic, on_delete=models.CASCADE)
    media = models.FileField(upload_to=upload_to_Thread, max_length=256, blank=True, default='threads/default.jpg')

    def __str__(self):
        return "user_" + str(self.pk) + "_" + str(self.title)


class Post(models.Model):
    content = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    threadID = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return "thread_" + str(self.threadID.pk) + "_" + str(self.author)

