from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from .models import MAIL,User
from django.contrib.auth.decorators import login_required
from .helpmodules.huf import handle_uploaded_file
from os.path import split
import time

class MAILFORM(forms.Form):
    touser=forms.CharField(max_length=500,label="To:")
    content=forms.CharField(max_length=10000,label="Content:",widget=forms.Textarea)
    attached_file=forms.FileField(required=False)

class NEWACCOUNTFORM(forms.Form):
    username=forms.CharField(max_length=500,label="Username:")
    password=forms.CharField(max_length=100,label="Password:",widget=forms.PasswordInput)
    password2=forms.CharField(max_length=100,label="Password(again):",widget=forms.PasswordInput)

    first_name=forms.CharField(max_length=78,label="First Name:")
    last_name=forms.CharField(max_length=89,label="Last Name:")
    email=forms.EmailField(max_length=100,label="Email adress(optional):",required=False)
    def clean_username(self):
        username1 = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username1)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username1
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("Email is taken")
        return email
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("Passwords must match.")
        return data

 
@login_required
def INBOXVIEW(request):
    if request.method=='POST':
        form=MAILFORM(request.POST,request.FILES)
        if form.is_valid():
            mail=MAIL(
                to_user=User.objects.get(username=form.cleaned_data['touser']),
                from_user=request.user,
                content=form.cleaned_data.get('content'),
                attachment=request.FILES.get('attached_file')
            )
            mail.save()
                
            return HttpResponseRedirect('/inbox/')
    else:
        form=MAILFORM()
    template=loader.get_template('gmsapp/inbox.html')
    context={
        'MAILS':MAIL.objects.all().order_by('-datepub'),
        'form':form,
        'curuser':request.user,
    
        }
    return HttpResponse(template.render(context,request))

def NEWACCOUNTVIEW(request):
    if request.method=='POST':
        form=NEWACCOUNTFORM(request.POST)
        if form.is_valid():
            user=User.objects.create_user(form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            user.save()
            return HttpResponseRedirect('/login/')
    else:
        form=NEWACCOUNTFORM()
    template=loader.get_template('gmsapp/newaccount.html')
    context={
        'form':form
    }
    return HttpResponse(template.render(context,request))
def MMVIEW(request):
    template=loader.get_template('gmsapp/mymails.html')
    query_set_valid=MAIL.objects.filter(from_user=request.user).order_by('-datepub')
    context={
        'MYMAILS':query_set_valid
    }
    return HttpResponse(template.render(context,request))
def OPTVIEW(request):
    template=loader.get_template('gmsapp/options.html')
    return HttpResponse(template.render({},request))
def STVIEW(request):
    template=loader.get_template('gmsapp/stview.html')
    curtime=time.ctime(time.time())
    context={
        'curtime':curtime

        }
    return HttpResponse(template.render(context,request))

