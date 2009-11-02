## Has functions needed for establishing connections between users and keeping track of all the data..
#

import django.http
from django.template import Template, Context
from django import forms
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from alpha.models import Connections, FreeList, UserList,Users

##Given a session-id, let's populate the Session tables with all data we need to keep track of.
## NOTE: Strictly this needs to be a per-uid table not per-session id. BUT no harm in keeping some fields anyways :)

################################################################################

def get_uid(sid) :
    """
    Generates a user-id (uid) given a session-id. This needs to be an invertible function. 
    """
    return sid

def get_sid(uid) :
    """uid to sid"""
    return uid

################################################################################

def get_chat_partner(uid) :
    """Search for values of uid which are there in the Free list
    """
    freelist = Users.objects.filter(status="FREE").orderby("score1")
#    freelist = Users.objects.get(status="FREE")

    if len(freelist) == 0 :
        return -1 ## No user to chat with..
    
    #Select highest scoring user to chat with..currently just return 1st for testing..
    uid=str(freelist[0].uid) 
    
    return uid

################################################################################
def send_message(msg, uid) :
    """
    sender pushes message (msg) to its chat partner. This function must figure out whom to send it to and all of that
    Either use message queues or brute-force refresh or whatever..
    """
    #get chatpartner
    try:
        u = Users.objects.get(uid=uid)
    except Users.DoesNotExist :
        return -1 ##Could not send because user not found. maybe diconnected?
    
    partner=str(u.partner)
    #put it in his queue
    try:
        p = Users.objects.get(uid=partner)
    except Users.DoesNotExist :
        return -1 ##Could not send because user not found. maybe diconnected?

    #put msg in the msg queue
    p.mq0=msg

    return partner

################################################################################

def get_messages(uid) :
    """Get the messages for this uid"""
    try:
        u=Users.objects.get(uid=uid)
    except Users.DoesNotExist:
        return ''

    return str(u.mq0)

################################################################################
    
def register_user(request) :
    """
    Performs various tasks like updating tables when a user connects. Only for new users
    """
    sid = request.COOKIES['sessionid']
    u=get_uid(sid)
    try : 
        q=Users.objects.get(uid=u)
    except Users.DoesNotExist :
        #Create the new user.
        u1 = Users(uid=u, status = "FREE", partner ='', score1 ='0' , score2='0', mq0 ='', mq1 ='' , time = '000')

        u1.save()
        print "USER CREAT"+u1.__str__()
        return 1
    #What happens when user is already there?
    else :
        q.status="FREE"
        q.partner=''
        q.score1=''
        q.score2=''
        q.mq0=''
        q.mq1=''
        q.time='000'
        print "USER UPDAT"+q.__str__()
        return 1

################################################################################

def sid_active(sid) :
    """means that user is already chatting. No need to do anything
    Check this by iterating over the dictionary of uid:sid pairs.
    """
    try:
        u = Users.objects.get(uid=sid)
    except Users.DoesNotExist :
        return -1
    else :
        if u.status=="ACTIVE":
            return 1
        else :
            return -1

################################################################################
def first_contact(request) :
    """Determine if following conditions hold:
    1. User has just logged in.
    2. Anon opens the chat tab.
    Need to update connection tables and userlists etc.
    """
    sid = request.COOKIES['sessionid']
    uid = get_uid(sid)
    add_to_userlist(uid)
    chat_uid = get_chat_partner(uid)
    ### Returns -1 if fails..
    if chat_uid == -1 : 
        """ Try again after some time
        """
        pass

    else :
        pass

################################################################################

def disconnect(uid) :
    """uid has disconnected.."""
    try :
        u = Users.objects.get(uid=uid)

        if str(u.status) == 'ACTIVE' :
            partner=str(u.partner)
            p=Users.objects.get(uid=partner)
            p.status='FREE'
            
        u.delete()
    except :
        return 1 #no entry found so already disconnected..
    else :
        return 1

################################################################################

def init() :
    ulist=Users.objects.all()
    for q in ulist :
        q.status="FREE"
        q.partner=''
        q.score1=''
        q.score2=''
        q.mq0=''
        q.mq1=''
        q.time='000'
