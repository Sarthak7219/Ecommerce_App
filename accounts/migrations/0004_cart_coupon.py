# Generated by Django 4.2.1 on 2023-07-09 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_coupon'),
        ('accounts', '0003_cart_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.coupon'),
        ),
    ]