# Generated by Django 3.2.15 on 2022-10-02 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0003_alter_album_category_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='category_filter',
            field=models.CharField(choices=[('General', 'General'), ('Animals', 'Animals'), ('Architecture', 'Architecture'), ('Baby', 'Baby'), ('Commercial', 'Commercial'), ('Fashion', 'Fashion'), ('Landscape', 'Landscape'), ('Portrait', 'Portrait'), ('Wedding', 'Wedding'), ('Sports', 'Sports')], default='General', max_length=32),
        ),
    ]
