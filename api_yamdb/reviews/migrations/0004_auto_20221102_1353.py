# Generated by Django 2.2.16 on 2022-11-02 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20221102_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='category',
        ),
        migrations.AddField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Categories'),
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='genres', to='reviews.Genre'),
        ),
    ]