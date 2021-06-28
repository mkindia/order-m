# Generated by Django 3.1.6 on 2021-06-25 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makeorders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='Party_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sentorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Transfer To', 'Transfer To Consignee')], default='Delivered', max_length=30, null=True),
        ),
    ]