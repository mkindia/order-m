# Generated by Django 3.1.7 on 2021-05-29 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makeorders', '0007_orders_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='unit',
            field=models.CharField(choices=[('Bag', 'Bag'), ('Box', 'Box'), ('Dozen', 'Dozen'), ('Gms.', 'Gms.'), ('Kgs.', 'Kgs.'), ('Meter', 'Meter'), ('Pcs.', 'Pcs.'), ('Roll', 'Roll'), ('Liter', 'Liter'), ('Carton', 'Carton')], default='Carton', max_length=30),
        ),
    ]
