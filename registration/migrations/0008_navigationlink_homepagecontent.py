# Generated by Django 4.2 on 2025-01-29 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_delete_homepagecontent_delete_navigationlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HomePageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_title', models.CharField(max_length=200)),
                ('hero_subtitle', models.CharField(max_length=200)),
                ('hero_description', models.TextField()),
                ('footer_content', models.TextField()),
                ('navigation_links', models.ManyToManyField(related_name='home_pages', to='registration.navigationlink')),
            ],
        ),
    ]
