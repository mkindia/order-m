# Generated by Django 3.1.7 on 2021-05-14 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makeorders', '0009_auto_20210514_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='Delivered', max_length=30, null=True),
        ),
    ]
