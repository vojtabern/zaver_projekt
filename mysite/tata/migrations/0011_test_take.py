# Generated by Django 4.1.1 on 2022-11-07 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tata', '0010_remove_psycholog_education_vzdelani_psycholog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id_test', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, null=None)),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tata.user')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Take',
            fields=[
                ('id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('test_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tata.test')),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tata.user')),
            ],
        ),
    ]
