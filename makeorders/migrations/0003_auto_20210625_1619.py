# Generated by Django 3.1.6 on 2021-06-25 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makeorders', '0002_auto_20210625_1614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='Party_id',
            new_name='party_id',
        ),
    ]
