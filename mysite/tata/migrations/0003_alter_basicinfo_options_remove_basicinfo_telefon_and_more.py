# Generated by Django 4.1.1 on 2022-09-09 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tata', '0002_alter_basicinfo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basicinfo',
            options={'ordering': ['uryvek']},
        ),
        migrations.RemoveField(
            model_name='basicinfo',
            name='telefon',
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='uryvek',
            field=models.TextField(default=''),
        ),
    ]
