# Generated by Django 3.2 on 2021-07-23 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
