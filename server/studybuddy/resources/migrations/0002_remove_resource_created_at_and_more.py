# Generated by Django 5.0.4 on 2024-09-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='description',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='file',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='subdomain',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='subject',
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_type',
            field=models.CharField(choices=[('pdf', 'PDF'), ('youtube', 'YouTube Link'), ('website', 'Website Link')], max_length=10),
        ),
        migrations.AlterField(
            model_name='resource',
            name='url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='Bookmark',
        ),
    ]
