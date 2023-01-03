from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
# Create your views here.

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if UD.is_valid and PD.is_valid():
            USO=UD.save(commit=False)
            pw=UD.cleaned_data['password']
            USO.set_password(pw)
            USO.save()

            PFO=PD.save(commit=False)
            PFO.user=USO
            PFO.save()
            return HttpResponse('registration successfully')


    return render(request,"registration.html",d)