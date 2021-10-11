from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,authenticate
from .froms import SignupForm,LoginForm,BlogForm
from django.contrib import messages
from django.contrib.auth import login,logout
from .models import Post
from django.contrib.auth.models import Group


def home(request):
    post = Post.objects.all()
    return  render(request, 'app/home.html',{'post':post})

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        user = request.user
        full_name= user.get_full_name()
        grp = user.groups.all()
        return render(request, 'app/dashboard.html', {'post':post,'full_name':full_name,'groups':grp})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def user_signup(request):
    if request.method =='POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            group = Group.objects.get(name='User')
            user.groups.add(group)
            fm = SignupForm()
            messages.warning(request,'Account Created !!!')
    else:
        fm = SignupForm()
    return render(request, 'app/signup.html',{'form':fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                pwd = fm.cleaned_data['password']
                user = authenticate(username=uname, password=pwd)
                if user is not None:
                    login(request, user)
                    messages.warning(request,'Logged in successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm = LoginForm()

        return render(request, 'app/login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')

def add_blog(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            fm = BlogForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                reg = Post(title=title, desc=desc)
                reg.save()
                messages.warning(request, 'Your Blog is Added !!')

                fm = BlogForm()
        else:
            fm = BlogForm()
        return render(request,'app/addblog.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')

def update_blog(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            key = Post.objects.get(pk=id)
            fm = BlogForm(request.POST, instance=key)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/dashboard/')

        else:
            key = Post.objects.get(pk=id)
            fm = BlogForm(instance=key)
        return render(request,'app/updateblog.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

def delete_blog(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            key = Post.objects.get(pk=id)
            key.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')