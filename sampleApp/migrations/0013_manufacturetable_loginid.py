# Generated by Django 5.1.3 on 2025-01-20 03:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleApp', '0012_alter_feedback_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturetable',
            name='LOGINID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sampleApp.logintable'),
        ),
    ]
