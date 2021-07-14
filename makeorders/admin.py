from django.contrib import admin

# Register your models here.
from .models import Clients, Consignees, Orders, Sentorder, Items, Item_Groups


@admin.register(Clients, Consignees, Orders, Sentorder, Items, Item_Groups)
class mydata(admin.ModelAdmin):
    pass
