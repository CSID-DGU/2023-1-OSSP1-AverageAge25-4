#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticesProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        if sys.argv[2] == 'react':
            project_root = Path(os.getcwd()).parent
            os.chdir(os.path.join(project_root, "Frontend", "dongguk-notice-app"))
            print(os.path.join(project_root, "Frontend", "dongguk-notice-app"))
            os.system("npm start")
            os.chdir(os.path.join(project_root, "Backend"))
            sys.argv.pop(2)
    except IndexError:
        execute_from_command_line(sys.argv)
    else:
        execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
