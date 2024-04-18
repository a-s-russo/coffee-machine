"""Module providing a utility function."""

from time import sleep


def print_processing_indicator(repetitions=3):
    """Prints a processing indicator."""
    for _ in range(repetitions):
        sleep(1)
        print('...')
