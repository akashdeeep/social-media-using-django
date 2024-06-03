from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, LikePost, Followers
from itertools import chain


@login_required(login_url='signin')
def index(requests):
    user_object = User.objects.get(username=requests.user.username)
    user_profile = Profile.objects.get(user=user_object)
    followings = Followers.objects.filter(follower=requests.user)
    filter_post = []
    print(len(followings))
    for following in followings:
        post = Post.objects.filter(user=following.user)
        filter_post.append(post)
    posts = list(chain(*filter_post))
    # posts = Post.objects.filter(user=user_object.username)
    return render(requests, 'index.html', {'user_profile': user_profile, 'posts': posts})


def signup(requests):
    if requests.method == 'POST':
        username = requests.POST['username']
        email = requests.POST['email-box']
        password1 = requests.POST['password-box']
        password2 = requests.POST['password_box2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(requests, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(requests, 'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(email=email, username=username, password=password1)
                user.save()
                user_login = auth.authenticate(username=username, password=password1)
                auth.login(requests, user_login)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, profile_id=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(requests, 'The given passwords dont match')
            return redirect('signup')
        return HttpResponse('hello')
    else:
        return render(requests, 'signup.html')


def signin(requests):
    if requests.method == "POST":
        username = requests.POST['username']
        password = requests.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(requests, user)
            return redirect('/')
        else:
            messages.info(requests, 'credentials are invalid')
            return redirect('signin')

        '''user_model = User.objects.get(username=username)
        if user_model is not None:
            if user_model.password == password:
                HttpResponse('Correct User Password')
            else:
                messages.info(requests, 'password doesnt match')
                return redirect('signin')
        else:
            messages.info(requests, 'username doesnt exists')
            return redirect('signin')'''
    else:
        return render(requests, 'signin.html')


@login_required(login_url='signin')
def logout(requests):
    # Add feature: Ask for confirmation for logout
    auth.logout(requests)
    return redirect(signin)


@login_required(login_url='signin')
def settings(requests):
    user_profile = Profile.objects.get(user=requests.user)
    if requests.method == "POST":
        user_profile.bio = requests.POST['bio']
        user_profile.location = requests.POST['location']
        if requests.FILES.get('profile_pic') is None:
            user_profile.profile_image = user_profile.profile_image
        else:

            user_profile.profile_image = requests.FILES.get('profile_pic')
        user_profile.save()
        return redirect('/')

    return render(requests, 'settings.html', {"user_profile": user_profile})


@login_required(login_url='signin')
def upload(requests):
    if requests.method == 'POST':
        user = requests.user.username
        image = requests.FILES.get('image')
        caption = requests.POST['caption']
        post = Post.objects.create(user=user, image=image, caption=caption)
        post.save()
        return redirect('/')
    return render(requests, 'upload.html')


def like_post(requests):
    # print(post_id)
    username = requests.user.username
    post_id = requests.GET.get('post_id')
    post = Post.objects.filter(id=post_id)[0]
    print(2)
    # post = requests.
    postlike = LikePost.objects.filter(username=username, post_id=post_id)

    if len(postlike) == 0:
        like = LikePost.objects.create(username=username, post_id=post_id)
        like.save()
        post.likes_count += 1
        post.save()
        return redirect('/')
    else:
        postlike[0].delete()
        # print(post.likes_count)
        post.likes_count = post.likes_count - 1
        post.save()
        return redirect('/')


def profile(requests, name):
    user = User.objects.get(username=name)
    profile = Profile.objects.get(user=user)
    print(profile.profile_image)
    posts = Post.objects.filter(user=name)
    no_posts = len(posts)
    context = {'user': user, 'profile': profile, 'posts': posts, 'no_posts': no_posts}
    return render(requests, 'profile.html', context)


def follow(requests):
    # Do the same for "following"
    follower = requests.user
    user_name = requests.GET.get('user_name')
    user = User.objects.filter(username=user_name)[0]
    user_profile = Profile.objects.filter(user=user)[0]
    follow = Followers.objects.filter(user=user.username, follower=follower.username)
    # if user == follower, following option should be disabled
    if len(follow) == 0:
        create_follow = Followers.objects.create(user=user.username, follower=follower.username)
        create_follow.save()
        user_profile.followers += 1
        user_profile.save()
        return redirect('/profile/' + user_name)

    else:
        follow[0].delete()
        user_profile.followers -= 1
        user_profile.save()
        return redirect('/profile/' + user_name)


def search(requests):
    search = requests.GET.get('search')
    usernames = User.objects.filter(username__icontains=search)
    return render(requests, 'search.html', {'usernames': usernames})
# def comments(requests):
#     if requests.method() == 'POST':
#
