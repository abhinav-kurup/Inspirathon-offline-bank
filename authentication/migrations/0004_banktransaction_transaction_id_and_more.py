# Generated by Django 4.2.6 on 2023-10-07 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_banktransaction_type_banktransaction_wallet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='wallettransaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
