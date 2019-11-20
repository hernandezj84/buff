from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token


class UserHelper(object):
    """Methods of user creation helper"""

    def get_group(self, name):
        """ Get group object by given name """
        return Group.objects.get(name=name)

    def get_token(self, email):
        """Get token from email"""
        token = Token.objects.get_or_create(user=email)
        return token

    def create_commerce(self, email, password):
        """Cretes commerce"""
        group = self.get_group("commerce")
        commerce = User()
        commerce.username = email
        commerce.email = email
        commerce.set_password(password)
        commerce.save()
        group.user_set.add(commerce)
        token = self.get_token(email)
        return token
