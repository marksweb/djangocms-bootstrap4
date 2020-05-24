# Generated by Django 2.2.12 on 2020-05-24 02:55

from django.db import migrations, models
import djangocms_bootstrap4.contrib.bootstrap4_grid.constants
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4_grid', '0004_remove_bootstrap4gridcolumn_column_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='bootstrap4gridcontainer',
            name='name',
            field=models.CharField(blank=True, help_text='Shown only to the admins in the structure mode for better orientation', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='bootstrap4gridcontainer',
            name='container_type',
            field=enumfields.fields.EnumField(default='container', enum=djangocms_bootstrap4.contrib.bootstrap4_grid.constants.GridContainerType, max_length=255, verbose_name='Container type'),
        ),
    ]
