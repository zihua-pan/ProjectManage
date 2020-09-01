from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Project)
admin.site.register(Department)
admin.site.register(Product)
admin.site.register(Task)
admin.site.register(Version)
admin.site.register(Progress)