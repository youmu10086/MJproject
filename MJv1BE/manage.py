#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # 获取当前文件的目录
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # # 将 apps 目录添加到 Python 的模块搜索路径
    # sys.path.append(os.path.join(current_dir, 'apps'))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MJv1BE.settings')

    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as RunServerCommand
        RunServerCommand.default_addr = '127.0.0.1'
        RunServerCommand.default_port = '8000'
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()