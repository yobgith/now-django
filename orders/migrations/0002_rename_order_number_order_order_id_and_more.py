# Generated by Django 4.2.2 on 2024-06-14 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_number',
            new_name='order_id',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='order',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='payment',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='user',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
