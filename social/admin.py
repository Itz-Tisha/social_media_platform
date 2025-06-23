from django.contrib import admin
from .models import webuser,web_post,followers,comments,notification
admin.site.register(web_post)
admin.site.register(webuser)
admin.site.register(followers)
admin.site.register(comments)
admin.site.register(notification)
# Register your models here.
