# Generated by Django 3.1.7 on 2021-05-14 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makeorders', '0008_orders_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='Sent', max_length=30, null=True),
        ),
    ]
