# Generated by Django 3.0.5 on 2020-08-02 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20200725_2310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
    ]
