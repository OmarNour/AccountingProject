from django.contrib.auth.models import User as DjangoUser, PermissionsMixin


class User(DjangoUser, PermissionsMixin):

    class Meta(object):
        DjangoUser._meta.get_field('email').__dict__['_unique'] = True

    def __str__(self):
        return self.username



