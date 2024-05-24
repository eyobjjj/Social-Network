from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile, Post, Comment, Save, Catagory, ChatMassage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .form import UserProfileForm, UserForm, PostForm, ChatMassageForm

from itertools import chain
@login_required(login_url='signin')
def index(request):

    userprofile = UserProfile.objects.get(user=request.user)
    all = userprofile.following.all()

    # massage show
    friends = userprofile.friend.all()
    message = ChatMassage.objects.filter(sender__user__in=friends, receiver__user=request.user, is_show=False)
    



    # posts = []
    # for i in all:
    #     post = Post.objects.filter(user=UserProfile.objects.get(user=i))
    #     posts.append(post)
    # posts = list(chain(*posts))
    posts = Post.objects.filter(user__user__in=all)

    save = Save.objects.filter(username=userprofile)
    savelist = []

    for i in save:
        savelist.append(i.post_id.id)

    print(message)
    context = {
        'userprofile':userprofile,
        'post':posts,
        'save':savelist,
        'message':message
    }
    return render(request, 'index.html', context)
def home(request):

    userprofile = UserProfile.objects.get(user=request.user)
    all = userprofile.following.all()

    posts = Post.objects.filter(user=UserProfile.objects.get(user=all))

    return render(request, 'home.html', {'posts':posts})


@login_required(login_url='signin')
def users(request):
    users = UserProfile.objects.all()
    #uu = UserProfile.objects.get(user= User.objects.get(username = request.user))
    uu = User.objects.get(username = request.user)

    for i in users:
        print(i)
        for ii in i.following.all():
            print(ii)

    return render(request, 'user_cards.html', {'users':users, 'uu':uu})



@login_required(login_url='signin')
def settings(request):
    userprofile = UserProfile.objects.get(user=request.user)
    u = User.objects.get(username=request.user)
    up_form = UserProfileForm(instance=userprofile)
    u_form = UserForm(instance=u)

    if request.method == 'POST':
        up_form = UserProfileForm(request.POST, request.FILES)
        u_form = UserForm(request.POST)

        if up_form.is_valid():
            print('pfoileeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

        if u_form.is_valid():
            print('pfoilrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')

        return redirect('settings')
    context = {
        'upform':up_form,
        'uform':u_form,
        'userprofile':userprofile,
    }
    return render(request, 'settings.html', context)

@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        userprofile = UserProfile.objects.get(user=request.user)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = userprofile
            post.save()
            return redirect('/')

    else:
        form = PostForm()

    return render(request, 'upload.html',{'form':form})

@login_required(login_url='signin')
def like_post(request):
    userprofile = UserProfile.objects.get(user=request.user)
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id = post_id)
    like_filter = Post.objects.filter(id=post_id, likes=userprofile)

    if like_filter:
        new_like = post.likes.remove(userprofile)
    else:
        new_like = post.likes.add(userprofile)
    
    return redirect('/')

@login_required(login_url='signin')
def dislike_post(request):
    userprofile = UserProfile.objects.get(user=request.user)
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id = post_id)
    like_filter = Post.objects.filter(id=post_id, dislikes=userprofile)

    if like_filter:
        new_like = post.dislikes.remove(userprofile)
    else:
        new_like = post.dislikes.add(userprofile)
    
    return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user = User.objects.get(username = pk)
    userprofile = UserProfile.objects.get(user=user)
    user_post = Post.objects.filter(user=userprofile)

    follow = UserProfile.objects.get(user=request.user)
    all = follow.following.all()
    if user in all:
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    save = Save.objects.filter(username=userprofile)
    context={
        'profile':userprofile,
        'post':user_post,
        'save':save,
        'button_text':button_text
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if  request.method == 'POST':
        user = User.objects.get(username=request.user)
        userp = UserProfile.objects.get(user=user)
        follow_user = request.POST['follow_user']
        friend = User.objects.get(username=follow_user)
        friendp = UserProfile.objects.get(user = friend)
        all = userp.following.all()
        print(follow_user)
        print(follow_user)
        print('----------------------')
        print(user)
        print(user)
#FollowCounter.objects.filter(username=username, follower=follow_user).first()
        if friend in all:
            userp.following.remove(friend)
            friendp.follower.remove(user)
        else:
            userp.following.add(friend)
            friendp.follower.add(user)         
        return redirect('/profile/'+follow_user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def postroom(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id = pk)
    user = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        message = request.POST['comment']
        newComment = Comment.objects.create(post_id = post, username = user, comment = message )
        newComment.save()

    context = {
        'post':post,
        'comments':comments
    }
    return render(request, 'postroom.html', context)

@login_required(login_url='signin')
def addsave(request, pk):
    userprofile = UserProfile.objects.get(user=request.user)
    post = Post.objects.get(id=pk)

    p = Save.objects.filter(post_id = post, username = userprofile)

    if p:
        save = Save.objects.get(post_id = post, username = userprofile)
        save.delete()
        return redirect('/')
    else:
        newsave = Save.objects.create(post_id = post, username = userprofile)
        newsave.save()
        return redirect('/')

@login_required(login_url='signin')
def chat(request):
    # userp = UserProfile.objects.get(user=request.user)
    # all = userp.friend.all()
    # chat = UserProfile.objects.filter(user__in = all)
    # message_count = []
    # for i in chat:
    #     message = ChatMassage.objects.filter(sender__user = i.user)
    #     message = message.filter(is_show=False)
    #     message_count.append([message])

    userp = UserProfile.objects.get(user=request.user)
    chat = []

    for i in userp.friend.all():
        c = UserProfile.objects.get(user = i)
        message = ChatMassage.objects.filter(sender__user = c.user)
        message = message.filter(is_show=False)
        chat.append([c,message])
    

    return render(request, 'chat.html', {'chat':chat})

@login_required(login_url='signin')
def singlechat(request, pk):
    user = User.objects.get(username=request.user)
    userp = UserProfile.objects.get(user=user)
    friend = User.objects.get(username=pk)
    friendp = UserProfile.objects.get(user=friend)

    message = ChatMassage.objects.filter(sender = userp, receiver = friendp) | ChatMassage.objects.filter(sender = friendp, receiver=userp)

    friend_filter = UserProfile.objects.filter(user=user, friend=friend)
    form = ChatMassageForm()
    if request.method == 'POST':

        if friend_filter:
            pass
        else:
            new_friend = userp.friend.add(friend)


        form = ChatMassageForm(request.POST, request.FILES)
        if form.is_valid():
            newMessage = form.save(commit=False)
            newMessage.sender = userp
            newMessage.receiver = friendp
            newMessage.save()
    context={
        'form':form,
        'message':message,
        'friendp':friendp,
        'userp':userp,
    }
    return render(request, 'singlechat.html', context)



























def signup(request):

    if  request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
    
        if password == password2 :
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()


                #login 
                user_login = authenticate(username=username, password=password)
                login(request, user_login)

                if user_login:
                    admin = User.objects.get(username = 'admin')                    
                    newUserProfile = UserProfile.objects.create(user=user)
                    newUserProfile.friend.add(admin)
                    newUserProfile.save()                    
                return redirect('settings')
        else:
            messages.info(request, 'password not matching')
            return redirect('signup')
        
    else:
        return render (request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'credentials invalid')
            return redirect('signin')
        
    else:
        return render (request, 'signin.html' )

@login_required(login_url='signin')
def logoutt(request):
    logout(request)
    return redirect('signin')