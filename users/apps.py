from django.apps import AppConfig
import signal

class UsersConfig(AppConfig):
    name = 'users'

    #def ready(self):
        #import users.signals

