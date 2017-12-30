from django.shortcuts import render
from . import forms
from django.contrib.auth import authenticate, login, logout,\
    update_session_auth_hash
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def logon(request):
    if request.method == 'POST':
        form = forms.Logon(request.POST)
        if form.is_valid():
            postdic = request.POST
            uid = postdic.get("uid")
            pwd = postdic.get("pwd")
            user = authenticate(username=uid, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/QuickLink/home/")
                else:
                    context = {}
                    context['hide_navbar_content'] = True  #hide nav content
                    context['msg'] = "Oops !! Your account has been disabled" 
                    context['url'] = "#"
                    context['bt'] = "Take me customer support"
                    return render(request,"common/failure.html",context)
            else:#if user is not None:
                context = {}
                context['hide_navbar_content'] = True  #hide nav content
                context['msg'] = "Oops !! UserID and Password don't match"
                context['url'] = "/QuickLink/auth/logon/"
                context['bt'] = "Take me to Logon"
                return render(request,"common/failure.html",context)
        else:#if form.is_valid():
            context = {}
            context['hide_navbar_content'] = True #hide nav content
            context['form'] = form
            return render(request,'authusr/logon.html',context)
    else: #if request.method == 'POST':
        form = forms.Logon
        context = {}
        context['hide_navbar_content'] = True #hide nav content
        context['form'] = form;
        return render(request, 'authusr/logon.html', context)
    
def register(request):
    if request.method == 'POST':
        form = forms.Registration(request.POST)
        if form.is_valid():
            postdic = request.POST
            user_name = postdic.get('uid')
            pwda = postdic.get('pwda')
            try:
                user = User.objects.create_user(password=pwda, username=user_name)
                user.is_staff = False
                user.is_active = True
                user.is_superuser = False
                user.save()
                context = {}
                context['hide_navbar_content'] = True  #hide nav content
                context['msg'] = "Congrats!!! You registered successfully!!" 
                context['url'] = "/QuickLink/auth/logon/"
                context['bt'] = "Take me to logon"
                return render(request,'common/success.html',context)
            except Exception as e:
                context = {}
                context['hide_navbar_content'] = True  #hide nav content
                context['msg'] = str(e)
                context['url'] = "#"
                context['bt'] = "Take me to customer care"
                return render(request,'common/failure.html',context)
        else:
            context = {}
            context['hide_navbar_content'] = True #hide nav content
            context['form'] = form
            return render(request,'authusr/register.html',context)
    else:
        form = forms.Registration()
        context = {}
        context['hide_navbar_content'] = True  #hide nav content
        context['form'] = form
        return render(request,'authusr/register.html',context)

@login_required
def changepwd(request):
    if request.method == 'POST':
        form = forms.ChangePassword(request.POST, user=request.user)
        if form.is_valid():
            postdic = request.POST
            pwda = postdic.get('pwda')
            try:
                request.user.set_password(pwda)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Important!
                context = {}
                context['hide_navbar_content'] = True  #hide nav content
                context['msg'] = "Congrats!!! You password changed successfully!!" 
                context['url'] = "/QuickLink/auth/logon/"
                context['bt'] = "Take me to logon"
                return render(request,'common/success.html',context)
            except Exception as e:
                context = {}
                context['hide_navbar_content'] = True  #hide nav content
                context['msg'] = str(e)
                context['url'] = "#"
                context['bt'] = "Take me to customer care"
                return render(request,'common/failure.html',context)
        else:
            context = {}
            context['hide_navbar_content'] = True #hide nav content
            context['form'] = form
            return render(request,'authusr/changepwd.html',context)
    else:
        form = forms.ChangePassword()
        context = {}
        context['hide_navbar_content'] = True  #hide nav content
        context['form'] = form
        return render(request,'authusr/changepwd.html',context)


@login_required    
def userlogout(request):
    context = {}
    context['hide_navbar_content'] = True  #hide nav content
    context['msg'] = "See you soon " + request.user.username 
    context['url'] = "/QuickLink/auth/logon/"
    context['bt'] = "Take me to logon"
    logout(request)
    return render(request,'common/success.html',context)
