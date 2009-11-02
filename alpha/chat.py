import django.http
from django.template import Template, Context
from django import forms
from django.shortcuts import render_to_response
import connection
from django.contrib.sessions.models import Session

 
class PostForm(forms.Form):
    """ Simple text area. Submit button in template """
    message = forms.CharField(widget=forms.Textarea())


def getMsg(request) :
    sid = request.COOKIES['sessionid']
    uid = connection.get_uid(sid)
    regUser = request.user
    print request.session.items()

    pending_message = ''
    d=''
    if request.method == 'POST' :
        form = PostForm(request.POST)

    else:
        if request.GET.get('getMsg', '') == 'True' :
            msg = repr(request.session.items())
            if msg!='' :
                pending_message = msg
                ##return some xml containing this pending message.. 
                #return connection.XMLize(pending_message,request)

                #Why the return - the pending msg is sent to the user requesting it, and since the client side js will update the page's contents using this new xml message, we do not need to do anything..
                # Below 2 lines for testing purposes using manual GET
                form = PostForm()
                return render_to_response('chat_template.html' , 
{'form':form , 'Conversation':'Stranger says: '+pending_message , 'session':repr(request.COOKIES) ,'user':regUser } )
            
            else : 
## We have no pending messages..May want to return some form of NULL xml?
                pass 

        elif request.GET.get('alive','') == 'True' :
            ##Act on keep-alive signals
            keep_alive(sid)
            # return nothing since we dont want to update page..
            return 

        elif request.GET.get('quit','') == 'True' :
            connection.disconnect(uid)
            return render_to_response('chat_template.html')

        ##Only display the empty form when none of the above..1st time visit etc
        
        else :
            form = PostForm()
            connection.register_user(request)

#Really dont need this. But this is how it also can be done if we do not wish to use the render_to_response method (which uses the template directory by default

#    fp = open ('/Users/prateeksharma/tp/first/alpha/chat_template.html')
#    t = Template(fp.read())
#    fp.close()
        
    if form.is_valid():
        message = form.cleaned_data['message']
        d=Session.objects.all()
        connection.send_message(message , uid)
        message = 'You Said: ' + message

    else: 
        message=''
    
    ##Now comes the matter of pending messages FOR this user...

    return render_to_response('chat_template.html' , 
{'form':form , 'Conversation': message , 'session':repr(request.session.items()), 'user':regUser } )

## Again an alternate way of doing this
#    html = t.render(Context({'form':form , 'Conversation': message, 'session':repr(request.session.items())}))
