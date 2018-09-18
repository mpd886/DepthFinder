from .csvformatter import CsvOutputter
from .paxformatter import PaxFormatter


CSV_FORMAT = "csv"
PAX_FORMAT = "pax"


class UnknownFormatterException(Exception):
    def __init__(self, formatter):
        super().__init__()
        self.formatter = formatter

    def __str__(self):
        return "Unknown output format '{}'".format(self.formatter)


def get_formatter(format):
    """
    Returns an object with a write method that takes an iterable of artifacts.Artifact objects
    :param format: Name of the format to output
    :return:
    """
    formatters = {CSV_FORMAT: CsvOutputter(),
                  PAX_FORMAT: PaxFormatter()}
    if format not in formatters:
        raise UnknownFormatterException(format)
    else:
        return formatters[format]