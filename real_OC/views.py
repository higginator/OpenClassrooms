from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

def some_func(request):
	return HttpResponse('dream xtreme')