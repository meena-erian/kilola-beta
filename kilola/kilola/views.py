from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


class Home(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/admin')


def confirm_email(self, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator\
            .check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect('https://kilola-ui.pages.dev/login')
    else:
        return HttpResponse('Invalid Token')
