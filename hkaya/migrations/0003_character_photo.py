# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkaya', '0002_auto_20171008_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]