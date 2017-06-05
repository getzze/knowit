# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from logging import NullHandler, getLogger
from six import text_type

from .property import Property

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Quantity(Property):
    """Quantity is a property with unit."""

    def __init__(self, name, unit, data_type=int, **kwargs):
        """Init method."""
        super(Quantity, self).__init__(name, **kwargs)
        self.unit = unit
        self.data_type = data_type

    def handle(self, value, context):
        """Handle value with unit."""
        if not isinstance(value, self.data_type):
            try:
                value = self.data_type(text_type(value))
            except ValueError:
                self.report(value, context)
                return

        return value * self.unit
