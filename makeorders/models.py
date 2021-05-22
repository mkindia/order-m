from django.db import models


# Create your models here.
class Clients(models.Model):
    party = models.CharField(max_length=30)
    address = models.CharField(max_length=30)

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.party


class Consignees(models.Model):
    party = models.ForeignKey(Clients, on_delete=models.CASCADE)
    consignee = models.CharField(max_length=30)
    station = models.CharField(max_length=30)    
    trasport = models.CharField(max_length=30)

    def __str__(self):
        return str( self.consignee )

class Items(models.Model):
    item_name=models.CharField(max_length=30)

class Orders(models.Model):
    consignees = models.ForeignKey(Consignees, on_delete=models.CASCADE)
    orderdate = models.DateField()
    item_name = models.CharField(max_length=30)
    item_price = models.FloatField(default=10.00)
    ordered_cartons = models.PositiveIntegerField(default=1)
    sent_cancel = models.PositiveIntegerField(default=0, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0, blank=True, null=True)
        

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
    cartons = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=30,blank=True, null=True, choices=sent_cancel,default='Delivered',)
    by = models.CharField(max_length=30, blank=True, null=True, choices=by,default='ByUs',)
   
    

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return str(self.orders)
