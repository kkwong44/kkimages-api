# Generated by Django 3.2.15 on 2022-10-02 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20221002_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['depart_id']},
        ),
        migrations.AddField(
            model_name='contact',
            name='depart_id',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
