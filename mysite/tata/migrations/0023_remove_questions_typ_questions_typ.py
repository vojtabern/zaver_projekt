# Generated by Django 4.1.1 on 2023-01-07 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tata', '0022_alter_questions_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='typ',
        ),
        migrations.AddField(
            model_name='questions',
            name='typ',
            field=models.ManyToManyField(to='tata.typ'),
        ),
    ]