import django.http
from django.template import Template, Context
from django import forms
from django.shortcuts import render_to_response
from django.contrib import auth

def index(request) :
    """Render index.html"""
    return render_to_response('index_template.html',) 
