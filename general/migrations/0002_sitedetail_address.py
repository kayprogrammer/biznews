# Generated by Django 4.1.2 on 2022-10-21 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitedetail',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
