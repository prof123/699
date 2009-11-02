# Create your views here.
import django.http

def print_Header(request) :
	if request.method == 'GET' :
		display = "You are using GET, arent you? <br>"
	
	headers=repr(request.META)
	getd = request.GET
	display = display + repr(getd) + "<br>"
	cookies = request.COOKIES
	display = display + "Your Cookies are : <br>"+ repr(cookies)

	html='<html><body> '+display+'</body></html>'
	return django.http.HttpResponse(html)
