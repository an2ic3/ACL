# Generated by Django 3.0.8 on 2020-07-30 18:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
        ('acl_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.AddField(
            model_name='service',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ACL',
        ),
    ]
