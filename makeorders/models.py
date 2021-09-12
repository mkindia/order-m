from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


# Create your models here.
class Clients(models.Model):
    party = models.CharField(max_length=30)
    station = models.CharField(max_length=30)
    transport = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
    comment = models.CharField(max_length=100,blank=True,null=True)
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.party


class Consignees(models.Model):
    party = models.ForeignKey(Clients, on_delete=models.CASCADE)
    consignee = models.CharField(max_length=30)
    party_consignee = models.PositiveIntegerField(blank=True,null=True)
    station = models.CharField(max_length=30)    
    transport = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
    comment = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return str( self.consignee )

class Item_Groups(models.Model):
    group_id = models.PositiveIntegerField(primary_key=True)
    group_name = models.CharField(max_length=30)
    group_des = models.CharField(max_length=100,blank=True,null=True)
    group_type = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str (self.group_name)


class Items(models.Model):
    item_group = models.ForeignKey(Item_Groups, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
    comment = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str (self.item_name )

class Orders(models.Model):

    units=[('Bag','Bag'),
    ('Box','Box'),
    ('Dozen','Dozen'),
    ('Gms.','Gms.'),
    ('Kgs.','Kgs.'),
    ('Meter','Meter'),
    ('Pcs.','Pcs.'),
    ('Roll','Roll'),
    ('Liter','Liter'),
    ('Carton','Carton'),]

    consignees = models.ForeignKey(Consignees, on_delete=models.CASCADE)
    party_id = models.PositiveIntegerField()
    orderdate = models.DateField()
    item_id = models.PositiveIntegerField()
    item_des=models.CharField(max_length=50,blank=True,null=True)
    item_price = models.FloatField()
    per = models.CharField(max_length=30,choices=units,default='Kgs.')
    qty = models.FloatField()
    unit = models.CharField(max_length=30,choices=units,default='Carton')
    sent_cancel = models.FloatField(default=0, blank=True, null=True)
    balance = models.FloatField(default=0, blank=True, null=True)
    sent_trs_id =models.PositiveIntegerField(blank=True,null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
    comment = models.CharField(max_length=100,blank=True,null=True)
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return str (self.item_id )


class Sentorder(models.Model):

    
    sent_cancel=[('Cancelled','Cancelled'),
                ('Sent','Sent'),
                ('Transfer','Transfer To Consignee'),]

    by = [('ByUs','ByUs'),
    ('ByParty','ByParty'),]            

    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    date = models.DateField()
    qty = models.FloatField()
    status = models.CharField(max_length=30,blank=True, null=True, choices=sent_cancel,default='Sent',)
    consignee_id=models.PositiveIntegerField(blank=True, null=True,)
    by = models.CharField(max_length=30, blank=True, null=True, choices=by,default='ByUs',)
    order_trs_id =models.PositiveIntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,editable=True)
    docket_number = models.CharField(max_length=50,blank=True,null=True)
    comment = models.CharField(max_length=100,blank=True,null=True)

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return str(self.orders)
