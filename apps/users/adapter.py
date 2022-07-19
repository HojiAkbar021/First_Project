from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def iduser(self, request):
        path = "/accounts/{username}/"
        return path.format(username=request.user.username)