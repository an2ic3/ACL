# Generated by Django 3.0.8 on 2020-07-30 19:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
        ('acl_manager', '0003_auto_20200730_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='service', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='service',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='service', to=settings.AUTH_USER_MODEL),
        ),
    ]
