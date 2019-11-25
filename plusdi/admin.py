from django.contrib import admin
from plusdi.models import Discount, Commerce, Client, ClientCategory, MatchDocument

# Register your models here.
admin.site.register(Discount)
admin.site.register(Commerce)
admin.site.register(Client)
admin.site.register(ClientCategory)
admin.site.register(MatchDocument)
