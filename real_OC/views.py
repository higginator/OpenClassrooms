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
		errors = form.errors
		return HttpResponse('BREAK')
		bldg = set_building(errors, form)
		num = set_num(errors, form)
		time = set_time(errors, form)
		day = set_day(errors, form)
		#try:
		rooms = determine_request(bldg, time, day, num)
		return render_to_response('test_rooms.html', RequestContext(request, {'rooms': rooms}))
			#return HttpResponseRedirect('/Thanks'
		#except NoInputError:
		#	form = SearchForm())
	else:
		form = SearchForm()
	return render_to_response('test_form.html', RequestContext(request, {'form': form}))

def hmm(request):
	return HttpResponse('Hi There')

def thanks(request):
	return HttpResponse('Thank You!!!')
