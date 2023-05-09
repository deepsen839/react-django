from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EventsModel(models.Model):
    event_name = models.CharField(max_length=255,null=True)
    data = models.TextField(null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255,null=True,blank=True)
    image = models.FileField(upload_to='event_images/',null=True,blank=True)
    is_liked = models.IntegerField(default=0)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    class Meta:
        db_table = "events"
        verbose_name = "Event"
        verbose_name_plural = "Events"
        


class EventsLiked(models.Model):
    events = models.ForeignKey(EventsModel,related_name='user_details',on_delete=models.DO_NOTHING) 
    likedby = models.ForeignKey(User,on_delete=models.DO_NOTHING) 
    class Meta:
        db_table = "events_liked"
        verbose_name = "Event Like"
        verbose_name_plural = "Event Likes"       