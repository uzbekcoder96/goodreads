# Generated by Django 4.0 on 2022-02-16 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_confirm_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='confirm_password',
        ),
    ]