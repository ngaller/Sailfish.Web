from google.appengine.ext import db

class UserProfile(db.Expando):
    """
    User account.
    Additional properties may be stored on the Expando object.
    """
    username = db.StringProperty()
    emails = db.StringListProperty()
    is_guest = db.BooleanProperty()
    is_admin = db.BooleanProperty()

    def put(self):
        """
        Method is overridden to add username to the list of emails, if it
        looks like an email.
        """
        if self.username.find("@") > -1 and self.emails.count(self.username) == 0:
            self.emails.append(self.username)
        db.Expando.put(self)

class UserAuthentication(db.Expando):
    """
    Information about specific authentication method used to log a user in.
    """
    # indicates the actual authentication method
    method = db.StringProperty()
    # authentication-specific identifier... eg email, login...
    identifier = db.StringProperty()
    user = db.ReferenceProperty(UserProfile)

def create_profile(username, authmethod, authid):
    """
    Create a user profile and associated authentication method.
    Return the UserAuthentication object.
    """
    user = UserProfile()
    user.username = username
    user.is_guest = False
    user.is_admin = False
    user.put()
    auth = UserAuthentication()
    auth.method = authmethod
    auth.identifier = authid
    auth.user = user
    auth.put()
    return auth

def get_user_byemail(email):
    return UserProfile.gql("WHERE emails=:1", email).get()

def get_auth(authmethod, authid):
    """
    Return UserAuthentication object corresponding to specific id / method,
    or None if not found.
    """
    return UserAuthentication.gql("WHERE method=:1 and identifier=:2", authmethod, authid).get()
