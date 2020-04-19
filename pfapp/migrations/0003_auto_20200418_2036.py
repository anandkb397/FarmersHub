# Generated by Django 3.0.3 on 2020-04-18 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pfapp', '0002_acctype_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acctype',
            old_name='User_id',
            new_name='u_id',
        ),
        migrations.RemoveField(
            model_name='acctype',
            name='roles',
        ),
        migrations.CreateModel(
            name='User_locations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30)),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfapp.Person')),
            ],
        ),
    ]
