# Generated by Django 3.0.3 on 2020-04-23 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfapp', '0003_auto_20200418_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=30)),
                ('dob', models.DateField(max_length=8)),
            ],
        ),
    ]
