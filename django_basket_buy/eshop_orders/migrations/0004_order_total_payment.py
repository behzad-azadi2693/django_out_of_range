# Generated by Django 3.2 on 2021-04-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop_orders', '0003_alter_order_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_payment',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
