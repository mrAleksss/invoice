# Generated by Django 4.1.5 on 2023-01-08 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_tag_invoice_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='tag',
            new_name='tags',
        ),
    ]