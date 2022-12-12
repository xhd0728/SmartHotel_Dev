# Generated by Django 4.1.3 on 2022-12-12 15:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.SmallIntegerField(default=0)),
                ('phone_num', models.CharField(max_length=11)),
                ('email', models.CharField(default=None, max_length=63)),
                ('last_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.level')),
            ],
        ),
    ]
