from django.contrib import admin

# Register your models here.
from .models import Clients, Consignees, Orders, Sentorder


@admin.register(Clients, Consignees, Orders, Sentorder)
class mydata(admin.ModelAdmin):
    pass
