# Generated by Django 4.1.1 on 2023-01-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tata', '0018_test_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Typ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(default='Typ otázky', max_length=45)),
            ],
            options={
                'ordering': ['typ'],
            },
        ),
    ]
