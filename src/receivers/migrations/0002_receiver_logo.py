# Generated by Django 4.1.5 on 2023-01-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receivers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiver',
            name='logo',
            field=models.ImageField(default='images/no_photo.png', upload_to=''),
        ),
    ]
