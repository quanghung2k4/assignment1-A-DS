from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from members.models import Member
# Create your views here.
def member(request):
    mymembers = Member.objects.all().values()
    template=loader.get_template('all_member.html')
    context={
        'mymembers': mymembers
    }
    return HttpResponse(template.render(context,request))

def details(request,id):
    mymember=Member.objects.get(id=id)
    template=loader.get_template('detail.html')
    context={
        'member':mymember
    }
    return HttpResponse(template.render(context,request))
def main(request):
    template=loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
    template=loader.get_template('testing.html')
    context={
        'fruits': ["Chuoi","Oi","Dao"]
    }
    return HttpResponse(template.render(context,request))



