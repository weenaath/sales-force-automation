#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# This block fixes the "usedforsecurity" crash in ReportLab
import hashlib
try:
    hashlib.md5(b'test', usedforsecurity=False)
except TypeError:
    # Your system doesn't support the security flag, so we strip it out
    original_md5 = hashlib.md5
    def patched_md5(*args, **kwargs):
        kwargs.pop('usedforsecurity', None)
        return original_md5(*args, **kwargs)
    hashlib.md5 = patched_md5

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
