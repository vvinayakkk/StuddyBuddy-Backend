# Generated by Django 5.0.4 on 2024-08-04 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testseries', '0004_test_shared_with'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='shared_with',
        ),
    ]
