from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.models import *
# Create your views here.
from django.core.mail import send_mail

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        
        if UD.is_valid() and PD.is_valid():
            
            pw=UD.cleaned_data['password']
            USO=UD.save(commit=False)
            USO.set_password(pw)
            USO.save()

            PFO=PD.save(commit=False)
            PFO.user=USO
            PFO.save()
            

            send_mail('User registration',
            'Regiistration is success full',
            'nagendra212001@gmail.com',
            [USO.email],fail_silently=False)
            
            return HttpResponse('registration successfully')

    return render(request,"registration.html",d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    return render(request,"user_login.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_info(request):
    username=request.session.get('username')
    USD=User.objects.get(username=username)
    PFD=Profile.objects.get(user=USD)
    d={'USD':USD,'PFD':PFD}
    return render(request,"profile_info.html",d)

@login_required
def changepassword(request):
    if request.method=='POST':
        username=request.session['username']
        password=request.POST['changepassword']
        USD=User.objects.get(username=username)
        USD.set_password(password)
        USD.save()
        return HttpResponseRedirect(reverse(user_login))
    return render(request,"changepassword.html")

def resetpassword(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['resetpassword']
        USO=User.objects.filter(username=username)
        if USO:
            USO[0].set_password(password)
            USO[0].save()
            return HttpResponseRedirect(reverse(user_login))
        else:
            return HttpResponse('username is not in the database')
    return render(request,"resetpassword.html")
    