# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='symbol',
            field=models.CharField(default='fa-book', help_text='Font Awesome icon name', max_length=50, null=True),
        ),
    ]