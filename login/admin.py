from django.contrib import admin
from .models import User

# Register your models here.
admin.site.unregister(User)
admin.site.register(User)
