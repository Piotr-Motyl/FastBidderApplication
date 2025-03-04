# Generated by Django 5.1.4 on 2024-12-10 12:34

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files_recording', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='file_path',
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(default=datetime.datetime(2024, 12, 10, 12, 33, 39, 512783, tzinfo=datetime.timezone.utc), upload_to='uploaded_files/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='file_type',
            field=models.CharField(choices=[('reference', 'Reference File'), ('working', 'Working File')], default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
    ]
