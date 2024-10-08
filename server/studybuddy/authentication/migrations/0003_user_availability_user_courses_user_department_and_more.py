# Generated by Django 5.0.6 on 2024-07-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_user_contact_remove_user_dob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='availability',
            field=models.CharField(blank=True, choices=[('Morning', 'Morning'), ('Evening', 'Evening'), ('Night', 'Night')], max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, choices=[('CSE', 'Computer Science'), ('EXTC', 'Electronics and Telecommunication'), ('MCA', 'Master of Computer Applications'), ('CE', 'Civil Engineering')], max_length=4),
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, to='authentication.user'),
        ),
        migrations.AddField(
            model_name='user',
            name='goals',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_study_methods',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='year',
            field=models.CharField(blank=True, choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')], max_length=1),
        ),
    ]
