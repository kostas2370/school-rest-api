# Generated by Django 4.0.3 on 2022-09-30 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_subject_assignments_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
