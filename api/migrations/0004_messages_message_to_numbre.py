# Generated by Django 4.0 on 2022-05-11 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='message_to_numbre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
