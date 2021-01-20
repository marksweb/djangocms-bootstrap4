# Generated by Django 3.1.4 on 2021-01-20 21:08

from django.db import migrations
import djangocms_bootstrap4.contrib.bootstrap4_grid.constants
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bootstrap4_grid', '0016_rename_fields_spacing_vertical_and_width_internal'),
    ]

    operations = [
        migrations.AddField(
            model_name='bootstrap4gridcontainer',
            name='spacing_horizontal',
            field=enumfields.fields.EnumField(default='none', enum=djangocms_bootstrap4.contrib.bootstrap4_grid.constants.GridContainerVerticalSpacingInternal, max_length=255, verbose_name='Horizontal spacing (padding)'),
        ),
        migrations.AddField(
            model_name='bootstrap4gridcontainer',
            name='spacing_vertical_internal',
            field=enumfields.fields.EnumField(default='none', enum=djangocms_bootstrap4.contrib.bootstrap4_grid.constants.GridContainerVerticalSpacingInternal, max_length=255, verbose_name='Vertical internal spacing'),
        ),
        migrations.AlterField(
            model_name='bootstrap4gridcontainer',
            name='spacing_vertical_external',
            field=enumfields.fields.EnumField(default='none', enum=djangocms_bootstrap4.contrib.bootstrap4_grid.constants.GridContainerVerticalSpacingInternal, max_length=255, verbose_name='Vertical external spacing'),
        ),
        migrations.AlterField(
            model_name='bootstrap4gridcontainer',
            name='width',
            field=enumfields.fields.EnumField(default='full-width', enum=djangocms_bootstrap4.contrib.bootstrap4_grid.constants.GridContainerWidthInternal, max_length=255, verbose_name='Width'),
        ),
    ]
