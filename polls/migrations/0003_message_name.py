# Generated by Django 5.1.3 on 2024-11-20 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='name',
            field=models.CharField(default='lol', max_length=200),
            preserve_default=False,
        ),
    ]