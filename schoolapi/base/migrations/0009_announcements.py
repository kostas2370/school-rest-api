# Generated by Django 4.0.3 on 2023-02-10 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_assignments_created_alter_assignments_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=1000)),
                ('image_post', models.ImageField(default='post_images/default.png', upload_to='post_images')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
