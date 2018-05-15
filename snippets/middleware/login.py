#encoding: utf-8

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginMiddleware(MiddlewareMixin):
	def __init__(self, get_response, *args, **kwargs):
        	self.get_response = get_response

	def process_request(self, request):
		if 'login' not in request.path and not request.user.is_authenticated:
			print "====== not in ======="
			return HttpResponseRedirect(reverse('login'))

