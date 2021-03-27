import re
import typing
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from knowit.property import Property


class Duration(Property[timedelta]):
    """Duration property."""

    duration_re = re.compile(r'(?P<hours>\d{1,2}):'
                             r'(?P<minutes>\d{1,2}):'
                             r'(?P<seconds>\d{1,2})(?:\.'
                             r'(?P<milliseconds>\d{3})'
                             r'(?P<microseconds>\d{3})?\d*)?')

    def __init__(self, *args: str, resolution: int or Decimal = 1, **kwargs):
        """Initialize a Duration."""
        super().__init__(*args, **kwargs)
        self.resolution = resolution

    def handle(self, value, context: typing.MutableMapping):
        """Return duration as timedelta."""
        if isinstance(value, timedelta):
            return value
        elif isinstance(value, int):
            return timedelta(milliseconds=int(value * self.resolution))
        try:
            return timedelta(milliseconds=int(Decimal(value) * self.resolution))
        except (ValueError, InvalidOperation):
            pass

        match = self.duration_re.match(value)
        if not match:
            self.report(value, context)
            return None

        params = {
            key: int(value)
            for key, value in match.groupdict().items()
            if value
        }
        return timedelta(**params)
