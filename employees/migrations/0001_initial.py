# Generated by Django 5.1.1 on 2024-09-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='middle name/patronymic')),
                ('position', models.CharField(max_length=100, verbose_name='position in the company')),
                ('company', models.CharField(max_length=100, verbose_name='company name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(blank=True, max_length=35, null=True, verbose_name='телефон')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'ordering': ('last_name', 'first_name', 'middle_name', 'email', 'phone'),
            },
        ),
    ]
