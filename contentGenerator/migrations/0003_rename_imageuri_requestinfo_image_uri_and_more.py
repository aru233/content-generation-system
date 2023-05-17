# Generated by Django 4.2.1 on 2023-05-16 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentGenerator', '0002_alter_requestinfo_imageuri_alter_requestinfo_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestinfo',
            old_name='imageUri',
            new_name='image_uri',
        ),
        migrations.AddField(
            model_name='requestinfo',
            name='image_status',
            field=models.CharField(default='Pending', max_length=10),
        ),
        migrations.AddField(
            model_name='requestinfo',
            name='text_status',
            field=models.CharField(default='Pending', max_length=10),
        ),
    ]
