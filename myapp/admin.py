from django.contrib import admin
from .models import Contact,User,Property,Inquiry
# Register your models here.
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(Property)
admin.site.register(Inquiry)