# Create your views here.
import django.http
from django import forms

##There was a lot more here!

def message(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MessageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # We dont need redirec in this case..
            #return HttpResponseRedirect('/thanks/')
		request.POST['message']
    else:
        form = MessageForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })
