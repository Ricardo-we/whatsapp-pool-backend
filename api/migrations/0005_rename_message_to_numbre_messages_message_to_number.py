# Generated by Django 4.0 on 2022-05-11 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_messages_message_to_numbre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='message_to_numbre',
            new_name='message_to_number',
        ),
    ]
