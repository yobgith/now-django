# Generated by Django 5.0.6 on 2024-05-27 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_avilable',
            new_name='is_available',
        ),
    ]