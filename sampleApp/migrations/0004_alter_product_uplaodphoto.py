# Generated by Django 4.2.16 on 2024-09-21 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleApp', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Uplaodphoto',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to='Media'),
        ),
    ]
