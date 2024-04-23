from django.contrib import admin
from .models import Followers, CustomUser

admin.site.register(CustomUser)
admin.site.register(Followers)
