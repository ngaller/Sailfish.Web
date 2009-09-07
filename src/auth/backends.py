from google.appengine.api import users
import models

class GaeBackend(object):
    """
    Authenticates using the GAE API
    """
    def get_current_user(self, request):
        """
        Current user
        """
        guser = users.get_current_user()
        if guser:
            auth = models.get_auth("GAE", guser.email())
            if not auth:
                auth = models.create_profile(guser.nickname(), "GAE", guser.email())
            auth.user.is_admin = users.is_current_user_admin()                
            return auth.user
        return None

    def get_login_url(self, request):
        """
        Login URL to redirect the user to - they should automatically be
        redirected to the current page when done.
        """
        return users.create_login_url(request.build_absolute_uri())

    def get_logout_url(self, request):
        if users.get_current_user():
            return users.create_logout_url(request.build_absolute_uri("/"))
        return None
