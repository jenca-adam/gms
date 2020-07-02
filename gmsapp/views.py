from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import MAIL,User

def inbox_view(request):
    template=loader.get_template('gmsapp/inbox.html')
    context={
        'MAILS':MAIL.objects.all(),
        }
    return HttpResponse(template.render(context,request))
