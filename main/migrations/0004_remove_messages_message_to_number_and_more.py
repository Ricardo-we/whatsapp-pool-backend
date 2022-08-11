# Generated by Django 4.0 on 2022-08-11 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_messages_message_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='message_to_number',
        ),
        migrations.AddField(
            model_name='messages',
            name='contact_info',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]