# Generated by Django 5.2.1 on 2025-05-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_deliveryaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_ready',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Обрабатывается'), ('assembled', 'Собран'), ('shipped', 'Передан')], default='processing', max_length=20),
        ),
    ]
