from django.db import models


# Create your models here.
class Clients(models.Model):
    party = models.CharField(max_length=30)
    station = models.CharField(max_length=30)
    transport = models.CharField(max_length=30)

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.party


class Consignees(models.Model):
    party = models.ForeignKey(Clients, on_delete=models.CASCADE)
    consignee = models.CharField(max_length=30)
    station = models.CharField(max_length=30)    
    transport = models.CharField(max_length=30)

    def __str__(self):
        return str( self.consignee )

class Items(models.Model):
    item_name = models.CharField(max_length=30)

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
    orderdate = models.DateField()
    item_name = models.CharField(max_length=30)
    item_price = models.FloatField(default=0.00)
    qty = models.FloatField(default=1)
    unit = models.CharField(max_length=30,choices=units,default='Carton',)
    sent_cancel = models.FloatField(default=0.00, blank=True, null=True)
    balance = models.FloatField(default=0.00, blank=True, null=True)
        

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return str (self.item_name )


class Sentorder(models.Model):

    
    sent_cancel=[('Cancelled','Cancelled'),
                ('Delivered','Delivered'),]

    by = [('ByUs','ByUs'),
    ('ByParty','ByParty'),]            

    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    date = models.DateField()
    qty = models.FloatField(default=1)
    status = models.CharField(max_length=30,blank=True, null=True, choices=sent_cancel,default='Delivered',)
    by = models.CharField(max_length=30, blank=True, null=True, choices=by,default='ByUs',)
   
    

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return str(self.orders)
