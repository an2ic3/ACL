# Generated by Django 3.0.8 on 2020-07-30 18:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acl_manager', '0002_auto_20200730_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='groups',
            field=models.ManyToManyField(related_name='service', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='service',
            name='users',
            field=models.ManyToManyField(related_name='service', to=settings.AUTH_USER_MODEL),
        ),
    ]
