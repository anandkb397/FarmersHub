# Generated by Django 3.0.3 on 2020-03-24 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acctype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acctypes', models.CharField(max_length=30)),
                ('roles', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Fruits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.CharField(max_length=30)),
                ('image', models.FileField(upload_to='static/images')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30)),
                ('pwd', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
            ],
        ),
    ]
