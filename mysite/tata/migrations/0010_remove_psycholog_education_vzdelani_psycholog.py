# Generated by Django 4.1.1 on 2022-11-07 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tata', '0009_user_remove_basicinfo_fk_psycholog_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='psycholog',
            name='education',
        ),
        migrations.AddField(
            model_name='vzdelani',
            name='psycholog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tata.psycholog'),
        ),
    ]
