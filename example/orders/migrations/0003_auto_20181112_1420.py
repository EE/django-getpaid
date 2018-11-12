# Generated by Django 2.0.7 on 2018-11-12 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_custompayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompayment',
            name='amount_refunded',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, verbose_name='amount refunded'),
        ),
        migrations.AddField(
            model_name='custompayment',
            name='fraud_message',
            field=models.TextField(blank=True, verbose_name='fraud message'),
        ),
        migrations.AddField(
            model_name='custompayment',
            name='fraud_status',
            field=models.CharField(choices=[('unknown', 'unknown'), ('accepted', 'accepted'), ('rejected', 'rejected'), ('check', 'check')], db_index=True, default='unknown', max_length=20, verbose_name='fraud status'),
        ),
        migrations.AddField(
            model_name='custompayment',
            name='refunded_on',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True, verbose_name='refunded on'),
        ),
        migrations.AlterField(
            model_name='custompayment',
            name='description',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='custompayment',
            name='external_id',
            field=models.CharField(blank=True, db_index=True, default='', max_length=64, verbose_name='external id'),
        ),
        migrations.AlterField(
            model_name='custompayment',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('in_progress', 'in progress'), ('accepted_for_proc', 'accepted for processing'), ('partially_paid', 'partially paid'), ('paid', 'paid'), ('cancelled', 'cancelled'), ('failed', 'failed'), ('refunded', 'refunded')], db_index=True, default='new', max_length=20, verbose_name='status'),
        ),
    ]