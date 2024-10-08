# Generated by Django 3.2.3 on 2024-07-19 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('testseries', '0004_test_shared_with'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('resource_type', models.CharField(choices=[('youtube', 'YouTube Link'), ('pdf', 'PDF File'), ('link', 'Anonymous Link')], max_length=10)),
                ('url', models.URLField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='resources/files/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testseries.chapter')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subdomain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testseries.subdomain')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testseries.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.resource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
