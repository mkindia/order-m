from django.contrib import admin

# Register your models here.
from .models import Clients, Consignees, Orders, Sentorder, Items


@admin.register(Clients, Consignees, Orders, Sentorder, Items)
class mydata(admin.ModelAdmin):
    pass
