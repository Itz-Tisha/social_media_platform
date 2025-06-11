from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index,name='index'),
     path('home/', views.home,name='home'),
      path('login/', views.login,name='login'),
      path('sign/', views.sign,name='sign'),
      path('post/',views.post,name='post'),
      path('people/',views.people,name='people'),
      path('follow_req/<int:user_id>',views.follow_req,name='follow_req'),
      path('following_list/',views.following_list,name='following_list'),
      path('unfollow/<int:f_id>',views.unfollow,name='unfollow'),
      path('followers_list/',views.followers_list,name='followers_list'),
      path('comment_box/<int:post_id>',views.comment_box,name='comment_box'),
      path('user_profile/',views.user_profile,name='user_profile'),
      path('hitted_like/<int:post_id>',views.hitted_like,name='hitted_like'),
      path('edit_profile/',views.edit_profile,name='edit_profile'),
      path('delete_post/<int:post_id>',views.delete_post,name='delete_post'),
      path('another_user<int:user_id>/',views.another_user,name='another_user'),
      path('logout/',views.logout,name='logout'),
      path('notifications/',views.notifications,name='notifications'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
