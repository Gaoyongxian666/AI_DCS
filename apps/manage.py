#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # 到模块，导入父文件夹
    AIDCS_Celery_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(AIDCS_Celery_dir)
    sys.path.append(AIDCS_Celery_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AI_DCS.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
