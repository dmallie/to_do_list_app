# Generated by Django 3.2.5 on 2022-12-02 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='user_name',
            new_name='username',
        ),
    ]
