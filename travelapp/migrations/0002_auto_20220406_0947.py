# Generated by Django 3.1.8 on 2022-04-06 04:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shotelname', models.CharField(max_length=100, null=True, unique=True)),
                ('shotelimg', models.ImageField(null=True, upload_to='images/')),
                ('shoteltype', models.CharField(max_length=100, null=True)),
                ('sstatus', models.IntegerField(default=1, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('screated_at', models.DateTimeField(auto_now_add=True)),
                ('supdated_at', models.DateTimeField(auto_now=True)),
                ('screated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='trips',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelapp.services'),
        ),
        migrations.DeleteModel(
            name='Hotel',
        ),
    ]
