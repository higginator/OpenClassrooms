from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from real_OC.forms import SearchForm
from django.template import RequestContext
from real_OC.helpers import set_building, set_num, set_time, set_day, determine_request

def some_func(request):
	return HttpResponse('dream xtreme')

"""
	 Once is_valid() returns True, the form data will be stored 
	 in the form.cleaned_data dictionary
"""
def home_page(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		#errors = form.errors
		#bldg = set_building(errors, form)
		#num = set_num(errors, form)
		#time = set_time(errors, form)
		#day = set_day(errors, form)
		bldg = request.POST.get('building')
		num = request.POST.get('number')
		time = request.POST.get('time')
		day = request.POST.get('day')
		ap = request.POST.get('ap')
		rooms = determine_request(bldg, time, day, num, ap)
		return render_to_response('test_rooms.html', RequestContext(request, {'rooms': rooms, 'form': form}))
	else:
		form = SearchForm()
	return render_to_response('test_form.html', RequestContext(request, {'form': form}))

def about(request):
	return render_to_response('about.html', RequestContext(request))

def buildings_list(request):
	return render_to_response('buildings_list.html', RequestContext(request))

def contact(request):
	return render_to_response('contact.html', RequestContext(request))

def get_data(request):
	if request.is_ajax():
		return HttpResponse('some string')
	else:
		return HttpResponse('another')