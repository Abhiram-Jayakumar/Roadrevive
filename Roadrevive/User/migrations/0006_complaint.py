# Generated by Django 5.1.2 on 2024-10-15 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0001_initial'),
        ('User', '0005_delete_complaint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Road Damage', 'Road Damage'), ('Potholes', 'Potholes'), ('Drainage Issues', 'Drainage Issues'), ('Other', 'Other')], max_length=50)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=150)),
                ('landmark', models.CharField(max_length=150)),
                ('pin', models.CharField(max_length=8)),
                ('image', models.ImageField(blank=True, null=True, upload_to='complaints/')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('date_filed', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Employee.employee')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
    ]
