# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 18:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojoSecrets_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Secrets',
            new_name='User',
        ),
    ]
