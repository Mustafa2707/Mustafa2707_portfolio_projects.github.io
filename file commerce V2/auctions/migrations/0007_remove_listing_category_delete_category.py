# Generated by Django 5.0.6 on 2024-08-01 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_category_listing_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
