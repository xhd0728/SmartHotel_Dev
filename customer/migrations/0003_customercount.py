# Generated by Django 4.1.3 on 2022-12-13 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
