import os
import json

TODOIST_API_KEY = None
BACKUP_DIR = None
BACKUP_SCHEDULES = None
APP_HOME = None
GRACE_PERIOD_MINUTES = None

def load_config(args):
    global TODOIST_API_KEY, BACKUP_DIR, BACKUP_SCHEDULES, APP_HOME, GRACE_PERIOD_MINUTES

    TODOIST_API_KEY = args.api_key or os.environ.get('TODOIST_API_KEY')
    if not TODOIST_API_KEY:
        raise ValueError("Todoist API key must be provided via -k argument or TODOIST_API_KEY environment variable")

    BACKUP_DIR = args.backup_dir or os.environ.get('DATA_BAK')
    if not BACKUP_DIR:
        raise ValueError("Backup directory must be provided via -d argument or DATA_BAK environment variable")

    APP_HOME = args.app_home or os.environ.get('CHECKIT_HOME') or os.path.expanduser('~/.checkit')
    os.makedirs(APP_HOME, exist_ok=True)

    schedule_file = args.schedule_file or os.path.join(APP_HOME, 'backup_schedules.json')
    with open(schedule_file, 'r') as f:
        BACKUP_SCHEDULES = json.load(f)

    GRACE_PERIOD_MINUTES = args.grace_period

def get_log_file():
    return os.path.join(APP_HOME, 'backup_check.log')
