# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial

from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from enumfields import EnumField
from six import python_2_unicode_compatible

from djangocms_bootstrap4.constants import DEVICE_SIZES
from djangocms_bootstrap4.fields import AttributesField
from djangocms_bootstrap4.fields import IntegerRangeField
from djangocms_bootstrap4.fields import TagTypeField
from djangocms_bootstrap4.helpers import mark_safe_lazy
from .constants import GRID_COLUMN_ALIGNMENT_CHOICES
from .constants import GRID_COLUMN_CHOICES
from .constants import GRID_CONTAINER_TYPE
from .constants import GRID_ROW_HORIZONTAL_ALIGNMENT_CHOICES
from .constants import GRID_ROW_VERTICAL_ALIGNMENT_CHOICES
from .constants import GRID_SIZE


@python_2_unicode_compatible
class Bootstrap4GridContainer(CMSPlugin):
    """
    Layout > Grid: "Container" Plugin
    https://getbootstrap.com/docs/4.0/layout/grid/
    """
    name = models.CharField(
        max_length=1024,
        null=True, blank=True,
        help_text=_('Shown only to the admins in the structure mode for better orientation'),
    )
    container_type = EnumField(
        GRID_CONTAINER_TYPE,
        default=GRID_CONTAINER_TYPE.DYNAMIC_WIDTH,
        verbose_name=_('Container type'),
        max_length=255,
    )
    tag_type = TagTypeField()
    attributes = AttributesField()

    def __str__(self) -> str:
        return str(self.pk)

    def get_short_description(self) -> str:
        if self.name:
            return self.name
        else:
            return f'({self.type.label})'


@python_2_unicode_compatible
class Bootstrap4GridRow(CMSPlugin):
    """
    Layout > Grid: "Row" Plugin
    https://getbootstrap.com/docs/4.0/layout/grid/
    """
    vertical_alignment = models.CharField(
        verbose_name=_('Vertical alignment'),
        choices=GRID_ROW_VERTICAL_ALIGNMENT_CHOICES,
        blank=True,
        max_length=255,
        help_text=mark_safe_lazy(_(
            'Read more in the <a href="{link}" target="_blank">documentation</a>.')
                .format(link='https://getbootstrap.com/docs/4.0/layout/grid/#vertical-alignment')
        ),
    )
    horizontal_alignment = models.CharField(
        verbose_name=_('Horizontal alignment'),
        choices=GRID_ROW_HORIZONTAL_ALIGNMENT_CHOICES,
        blank=True,
        max_length=255,
        help_text=mark_safe_lazy(_(
            'Read more in the <a href="{link}" target="_blank">documentation</a>.')
                .format(link='https://getbootstrap.com/docs/4.0/layout/grid/#horizontal-alignment')
        ),
    )
    gutters = models.BooleanField(
        verbose_name=_('Remove gutters'),
        default=False,
        help_text=_('Removes the marginal gutters from the grid.'),
    )
    tag_type = TagTypeField()
    attributes = AttributesField()

    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        column_count = len(self.child_plugin_instances or [])
        column_count_str = ungettext(
            '(1 column)',
            '(%(count)i columns)',
            column_count
        ) % {'count': column_count}

        return column_count_str


@python_2_unicode_compatible
class Bootstrap4GridColumn(CMSPlugin):
    """
    Layout > Grid: "Column" Plugin
    https://getbootstrap.com/docs/4.0/layout/grid/
    """
    column_type = models.CharField(
        verbose_name=_('Column type'),
        choices=GRID_COLUMN_CHOICES,
        default=GRID_COLUMN_CHOICES[0][0],
        blank=True,
        max_length=255,
    )
    column_alignment = models.CharField(
        verbose_name=_('Alignment'),
        choices=GRID_COLUMN_ALIGNMENT_CHOICES,
        blank=True,
        max_length=255,
    )
    tag_type = TagTypeField()
    attributes = AttributesField()

    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        text = ''
        classes = self.get_grid_values()
        if self.xs_col:
            text += '(col-{}) '.format(self.xs_col)
        else:
            text += '(auto) '
        if self.column_type != 'col':
            text += '.{} '.format(self.column_type)
        if classes:
            text += '.{}'.format(' .'.join(self.get_grid_values()))
        return text

    def get_grid_values(self):
        classes = []
        for device in DEVICE_SIZES:
            for element in ('col', 'order', 'offset', 'ml', 'mr'):
                size = getattr(self, '{}_{}'.format(device, element))
                if isinstance(size, int) and (element == 'col' or element == 'order' or element == 'offset'):
                    if device == 'xs':
                        classes.append('{}-{}'.format(element, int(size)))
                    else:
                        classes.append('{}-{}-{}'.format(element, device, int(size)))
                elif size:
                    if device == 'xs':
                        classes.append('{}-{}'.format(element, 'auto'))
                    else:
                        classes.append('{}-{}-{}'.format(element, device, 'auto'))

        return classes


IntegerRangeFieldPartial = partial(
    IntegerRangeField,
    blank=True,
    null=True,
    max_value=GRID_SIZE,
)

BooleanFieldPartial = partial(
    models.BooleanField,
    default=False,
)

# Loop through Bootstrap 4 device choices and generate
# model fields to cover col-*, order-*, offset-*, etc.
for size in DEVICE_SIZES:
    # Grid size
    Bootstrap4GridColumn.add_to_class(
        '{}_col'.format(size),
        IntegerRangeFieldPartial(),
    )
    # Grid ordering
    Bootstrap4GridColumn.add_to_class(
        '{}_order'.format(size),
        IntegerRangeFieldPartial(),
    )
    # Grid offset
    Bootstrap4GridColumn.add_to_class(
        '{}_offset'.format(size),
        IntegerRangeFieldPartial(),
    )
    # Grid margin left (ml)
    Bootstrap4GridColumn.add_to_class(
        '{}_ml'.format(size),
        BooleanFieldPartial(),
    )
    # Grid margin right (ml)
    Bootstrap4GridColumn.add_to_class(
        '{}_mr'.format(size),
        BooleanFieldPartial(),
    )
