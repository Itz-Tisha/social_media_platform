from django.db import models

# Create your models here.
   
# class event(models.Model):
#     event_name = models.CharField(max_length=20,unique=True)
#     location = models.CharField(max_length=50)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     date = models.DateField()
#     desc = models.CharField(max_length=50)
#     club_name = models.ForeignKey(club,on_delete=models.CASCADE)
#     attendee = models.IntegerField(default=0)
#     image = models.ImageField(upload_to='event_images/', blank=True, null=True)


class webuser(models.Model):
    name = models.CharField(max_length=50,unique=True)
    age = models.IntegerField()
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField( max_length=10)
    ac_type = [
        ('public', 'public'),
        ('private', 'private'),
    ]
    ac_type = models.CharField(max_length=10, choices=ac_type, default='public')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    #account type
    #bio
    

class web_post(models.Model):
    desc = models.CharField( max_length=50)
    date = models.DateField()
    likes = models.IntegerField()
    liked_by = models.ManyToManyField(webuser, related_name='liked_posts', blank=True)
    webuserId = models.ForeignKey(webuser, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    #comments
    #images
    

class followers(models.Model):
    webuser1Id = models.ForeignKey(webuser, on_delete=models.CASCADE,related_name='following')
    webuser2Id = models.ForeignKey(webuser, on_delete=models.CASCADE,related_name='followers')
    
class comments(models.Model):
    webpost = models.ForeignKey(web_post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    webuser = models.ForeignKey(webuser,on_delete=models.CASCADE)
    
class notification(models.Model):
    message = models.CharField(max_length=50)
    webuser1 = models.ForeignKey(webuser,on_delete=models.CASCADE,related_name='mainuser')
    webuser2 = models.ForeignKey(webuser,on_delete=models.CASCADE,related_name='inverseuser')
#notification 