# Generated by Django 3.2.3 on 2021-07-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makeorders', '0006_auto_20210721_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentorder',
            name='docket_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
