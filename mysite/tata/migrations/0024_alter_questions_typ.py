# Generated by Django 4.1.1 on 2023-01-09 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tata', '0023_remove_questions_typ_questions_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='typ',
            field=models.ManyToManyField(related_name='typy', to='tata.typ'),
        ),
    ]
