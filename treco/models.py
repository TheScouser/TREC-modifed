from django.db import models
from django.contrib.auth.models import User
from validator import *


# Create your models here.
class Track(models.Model):
    track_title = models.CharField(max_length=32, unique=True, primary_key=True)
    track_url = models.URLField(max_length=128)
    description = models.CharField(max_length=128, default="")
    genre = models.CharField(max_length=32, default="")

    def save(self, *args, **kwargs):
        super(Track, self).save(*args, **kwargs)

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return self.track_title


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, db_column='track_title')
    title = models.CharField(max_length=32, default="")
    task_url = models.URLField(max_length=128)
    description = models.CharField(max_length=128, default="")
    year = models.IntegerField(max_length=4)
    judgement_file = models.FileField(upload_to='judgement_files', validators=[])

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return self.track.track_title + ": " + self.title


class Researcher(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id')
    display_name = models.CharField(max_length=16, unique=True, primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', default="profile_pictures/default.png")
    website = models.URLField(max_length=128, default="")
    organization = models.CharField(max_length=64, default="")

    def save(self, *args, **kwargs):
        super(Researcher, self).save(*args, **kwargs)

    def delete_picture(self, *args, **kwargs):
        print ("Deleting")
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the file after the model
        storage.delete(path)
        self.profile_picture = "profile_pictures/default.png"
        super(Researcher, self).save(*args, **kwargs)

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return self.display_name


class Run(models.Model):

    RUNCHOICES = (('0', 'Automatic'), ('1', 'Manual'))
    QUERYCHOICES = (('0', 'Title'), ('1', 'Title and Description'), ('2', 'Description'), ('3', 'All'), ('4', 'Other'))
    FEEDBACKCHOICES = (('0', 'None'), ('1', 'Psuedo'), ('2', 'Relevance'),('3', 'Other'))

    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE, db_column='display_name')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default="")
    description = models.CharField(max_length=256, default="")
    result_file = models.FileField(upload_to='result_files', validators=[])
    run_type = models.CharField(max_length=1, choices=RUNCHOICES)
    query_type = models.CharField(max_length=32, choices=QUERYCHOICES)
    feedback_type = models.CharField(max_length=32, choices=FEEDBACKCHOICES)
    map = models.FloatField()
    p10 = models.FloatField()
    p20 = models.FloatField()

    def save(self, *args, **kwargs):
        super(Run, self).save(*args, **kwargs)

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return self.name



















