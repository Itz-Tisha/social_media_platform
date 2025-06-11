from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from .forms import signupform,loginform,postform,commentform,edit_profileform
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import webuser,web_post,followers,comments,notification
from django.utils import timezone
from django.contrib import messages 
from django.db.models import Q

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        try:
            name = request.session.get('username','')
            user = webuser.objects.get(name=name)
            return redirect('home')
        except webuser.DoesNotExist:
            return redirect('sign')  
    else:
        return redirect('sign')
    
    

def home(request):
    name = request.session.get('username','')
    email = request.session.get('email','')
    user = webuser.objects.get(name=name)
    user_followers = followers.objects.filter(webuser2Id=user).count()
    user_following = followers.objects.filter(webuser1Id=user).count()
    posts = web_post.objects.filter(Q(webuserId__ac_type='public') | Q(webuserId=user))
    for p in posts:
        print(p.post_image)
    return render(request,'home.html',{'name':name , 'posts':posts,'user_followers':user_followers, 'user_following':user_following})


def login(request):
    if request.method=='POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            user_password = form.cleaned_data['password']
            print(user_password)
            try:
                email = request.session.get('email','')
                user = webuser.objects.get(name=username)
                print(user.password)
                if user.password == user_password:
                    request.session['username'] = form.cleaned_data['name']
                    print(user.password)
                    return redirect('home')
                else:
                    print(1)
                    messages.error(request, "Invalid credentials. Please try again.")
            except webuser.DoesNotExist:
                print(2)
                messages.error(request, "User does not exist. Please sign up.")
        
    else:
        form = loginform()
    return render(request,'login.html',{'form':form})
        


def sign(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            
            password = form.cleaned_data['password']
            if webuser.objects.filter(name=name).exists():
                print("hello")
                messages.error(request, 'Email is already taken!')
                return redirect('sign')
        
            user = form.save(commit=False)
            user.save()
            request.session['email'] = email
            return redirect('login')
        
    else:
        form = signupform()
        
    
    return render(request,'sign.html',{'form':form})
        


def post(request):
    if request.method=='POST':
        
        form = postform(request.POST,request.FILES)
        if form.is_valid():
            posts = form.save(commit=False)
            date = timezone.now().date()
            posts.date = date
            posts.likes = 0
            name=request.session.get('username','')
            user = webuser.objects.get(name=name)
            posts.webuserId = user
            posts.save()
            return redirect('home')
        
    else:
        form = postform()
    
    return render(request,'postform.html',{'form':form})
    
    
    
def people(request):
    name = request.session.get('username','')
    email = request.session.get('email','')
    cur_user = webuser.objects.get(name=name)
    users = webuser.objects.exclude(name=name)
    followed_ids = followers.objects.filter(webuser1Id=cur_user).values_list('webuser2Id__id', flat=True)
    suggested_users = users.exclude(id__in=followed_ids)
    name = request.session.get('username','')
    return render(request, 'people.html', {'users': suggested_users,'name':name})



def follow_req(request,user_id):
    name = request.session.get('username', '')
    email = request.session.get('email', '')
    user1 = get_object_or_404(webuser, name=name)
    user2 = get_object_or_404(webuser, id=user_id)
    follow_relation = followers(webuser1Id=user1, webuser2Id=user2)
    follow_relation.save()
    notify = notification()
    notify.webuser1=user1
    notify.webuser2=user2
    notify.message= user1.name + " has started following " + user2.name;
    notify.save()
    return redirect('people')



def following_list(request):
    name = request.session.get('username', '')
    user = webuser.objects.get(name=name)
    following_id = followers.objects.filter(webuser1Id=user).values_list('webuser2Id',flat=True)
    users = webuser.objects.filter(id__in=following_id).exclude(id=user.id)
    is_following=True
    return render(request,'following.html',{'users':users,'is_following':is_following})
    
    
    
def unfollow(request,f_id):
    user = get_object_or_404(webuser,id=f_id)
    name=request.session.get('username','')
    email = request.session.get('email', '')
    cur_user = webuser.objects.get(name=name)
    followers_record = followers.objects.filter(webuser1Id=cur_user , webuser2Id=user)
    notify = notification()
    notify.webuser1=cur_user
    notify.webuser2=user
    notify.message= cur_user.name + " has unfollow " + user.name;
    notify.save()
    followers_record.delete()
    return redirect('following_list')



def followers_list(request):
    name = request.session.get('username', '')
    user = webuser.objects.get(name=name)
    followers_id = followers.objects.filter(webuser2Id=user).values_list('webuser1Id',flat=True)
    users = webuser.objects.filter(id__in=followers_id).exclude(id=user.id)
    is_following=False
    return render(request,'following.html',{'users':users,'is_following':is_following})


def comment_box(request,post_id):
    post = get_object_or_404(web_post, id=post_id)
    if request.method == 'POST':
        name = request.session.get('username','')
        user=webuser.objects.get(name=name)
        form = commentform(request.POST)
        if form.is_valid():
            user_comments = form.cleaned_data['comment']
            comment_model = form.save(commit=False)
            print(user_comments)
            comment_model.webpost = post
            comment_model.webuser = user
            comment_model.save()
            notify = notification()
            notify.webuser1=user
            notify.webuser2=post.webuserId
            notify.message= user.name + " has commented on  " + post.webuserId.name + "'s post";
            notify.save()
            return redirect('home')
    
    else:
        all_comments = comments.objects.filter(webpost=post).all()
        form = commentform()
    return render(request,'comment.html',{'form':form,'post':post,'all_comments':all_comments})



def user_profile(request):
    email = request.session.get('email','')
    name = request.session.get('username','')
    user = webuser.objects.get(name=name)
    posts = web_post.objects.filter(webuserId=user)
    post_count = web_post.objects.filter(webuserId=user).count()
    user_followers = followers.objects.filter(webuser2Id=user).count()
    user_following = followers.objects.filter(webuser1Id=user).count()
    ispublic=True
    user_itself=True
    return render(request,'user_profile.html',{'name':name , 'user':user,'posts':posts,'user_followers':user_followers, 'user_following':user_following,'post_count':post_count,'ispublic':ispublic,'user_itself':user_itself})


    
def hitted_like(request,post_id):
    post = get_object_or_404(web_post,id=post_id)
    name = request.session.get('username','')
    user = webuser.objects.get(name=name)
    if user not in post.liked_by.all():
        post.likes += 1
        post.liked_by.add(user)
        post.save()
        notify = notification()
        notify.webuser1=user
        notify.webuser2=post.webuserId
        notify.message= user.name + " has liked  " + post.webuserId.name + "'s post";
        notify.save()
    return redirect('home')



def edit_profile(request):
    name=request.session.get('username','')
    user = get_object_or_404(webuser, name=name)
    if request.method == 'POST':
        form = edit_profileform(request.POST,request.FILES,instance=user)
        if form.is_valid():
            new_user = form.save(commit=False)
            request.session['username'] = new_user.name
            new_user.save()
            return redirect('home')
    else:
        form = edit_profileform(instance=user)
    return render(request,'edit_profile_form.html',{'form':form})



def delete_post(request,post_id):
    post = get_object_or_404(web_post,id=post_id)
    post.delete()
    return redirect('user_profile')
            


def another_user(request,user_id):
    user = get_object_or_404(webuser,id=user_id)
    name = request.session.get('username','')
    posts = web_post.objects.filter(webuserId=user)
    post_count = web_post.objects.filter(webuserId=user).count()
    user_followers = followers.objects.filter(webuser2Id=user).count()
    user_following = followers.objects.filter(webuser1Id=user).count()
    user1_qs = webuser.objects.filter(name=name)
    user1 = user1_qs.first()  # returns first webuser or None
    user_itself = (user1 == user)


    ispublic=False
    if user.ac_type =='public':
        ispublic=True
    return render(request,'user_profile.html',{'name':name , 'user':user,'posts':posts,'user_followers':user_followers, 'user_following':user_following,'post_count':post_count,'ispublic':ispublic,'user_itself':user_itself})



def notifications(request):
    name = request.session.get('username','')
    cur_user = get_object_or_404(webuser,name=name)
    message = notification.objects.filter(
        Q(webuser1 = cur_user) | Q(webuser2 = cur_user)
    )
    return render(request,'notify.html',{'message':message})
    
    
    
def logout(request):
    request.session.flush()
    return redirect('login')



    