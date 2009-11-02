from django import  forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User


def register(request):
    """
    this function accepts user registration, handles errors and if data is clean then registers the user in the database. Finally if success redirects user to his chat page 
    """
    form = UserCreationForm()

    if request.method == 'POST':
        data = request.POST.copy()
        print data
        form = UserCreationForm(request.POST)

 #       errors = form.get_validation_errors(data)
 #       print errors

        if True:
            new_user = form.save(data) #TODO: catch errors and redirect
            new_user.save()
            print repr(new_user)
 #           new_user.n
            html='<html><body>'+'<p> SUCCESS </p>'+'</body></html>'
   
            return HttpResponse(html)
         #   return HttpResponseRedirect("chat/")
    else:
        data, errors = {}, {}
    html = '<html><body>'

    return render_to_response("registration/register.html", {
        'form' : form , 'data':data
    })
