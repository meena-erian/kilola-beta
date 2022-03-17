from django.http import HttpResponse, HttpResponseRedirect
from django.views import View


class Home(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/admin')