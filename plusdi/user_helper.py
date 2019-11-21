from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from plusdi.models import Commerce


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
        """Creates commerce"""
        group = self.get_group("commerce")
        commerce = User()
        commerce.username = email
        commerce.email = email
        commerce.set_password(password)
        commerce.save()
        group.user_set.add(commerce.id)
        token = self.get_token(commerce)
        commerce_profile = Commerce(commerce=commerce)
        commerce_profile.save()
        return token

    def create_client(self, email, password):
        """Creates client"""
        group = self.get_group("client")
        client = User()
        client.username = email
        client.set_password(password)
        client.save()
        group.user_set.add(client.id)
        token = self.get_token(client)
        return client
