from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from .models import MAIL,User
from django.contrib.auth.decorators import login_required

class MAILFORM(forms.Form):
    touser=forms.CharField(max_length=500,label="To:")
    content=forms.CharField(max_length=10000,label="Content:",widget=forms.Textarea)
@login_required
def inbox_view(request):
    if request.method=='POST':
        form=MAILFORM(request.POST)
        if form.is_valid():
            mail=MAIL(content=form.cleaned_data['content'],
            to_user=User.objects.get(username=form.cleaned_data['touser']),
            from_user=User.objects.get(username=request.user))
            mail.save()
            return HttpResponseRedirect('/inbox/')
        else:
            form=MAILFORM()
            
    template=loader.get_template('gmsapp/inbox.html')
    context={
        'MAILS':MAIL.objects.all().order_by('-datepub'),
        'form':MAILFORM,
        'curuser':request.user,
        }
    return HttpResponse(template.render(context,request))
