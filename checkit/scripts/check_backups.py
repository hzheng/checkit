import os
import logging
from datetime import datetime, timedelta

from croniter import croniter

from checkit.utils import config, notification

def setup_logging():
    logging.basicConfig(filename=config.get_log_file(), level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_last_check_time():
    last_check_file = config.get_last_check_file()
    if os.path.exists(last_check_file):
        with open(last_check_file, "r") as f:
            return datetime.fromisoformat(f.read().strip())
    return datetime.min + timedelta(hours=24) # add 1 day to avoid overflow

def update_last_check_time():
    last_check_file = config.get_last_check_file()
    with open(last_check_file, "w") as f:
        f.write(datetime.now().isoformat())

def should_backup_now(schedule, grace_period):
    now = datetime.now()
    cron = croniter(schedule, now)
    prev_backup = cron.get_prev(datetime)
    next_backup = cron.get_next(datetime)
    return prev_backup - grace_period <= now < next_backup + grace_period

def check_backups():
    grace_period_minutes = config.GRACE_PERIOD_MINUTES
    grace_period = timedelta(minutes=grace_period_minutes)
    max_age = timedelta(days=config.MAX_BACKUP_DAYS)
    last_check = get_last_check_time()
    now = datetime.now()
    
    lower_bound = max(last_check - grace_period, now - max_age)
    upper_bound = now + grace_period
    missing_backups = []

    for subdir, schedule in config.BACKUP_SCHEDULES.items():
        if not should_backup_now(schedule, grace_period):
            logging.info(f"No backup scheduled for {subdir} at this time (including grace period).")
            continue

        dir_path = os.path.join(config.BACKUP_DIR, subdir)
        if not os.path.exists(dir_path):
            logging.warning(f"Directory {dir_path} does not exist.")
            continue

        backup_found = False
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if lower_bound < file_mtime <= upper_bound:
                    logging.info(f"Backup found for {subdir}: {file} in ({lower_bound}, {upper_bound}]")
                    backup_found = True
                    break
        
        if not backup_found:
            missing_backups.append(subdir)
            logging.warning(f"Missing backup for {subdir} (including grace period {grace_period_minutes} minutes).")

    update_last_check_time()
    return missing_backups

def run():
    setup_logging()
    logging.info("Starting backup check")
    missing_backups = check_backups()
    if missing_backups:
        message = f"Missing backups for: {', '.join(missing_backups)}"
        logging.warning(message)
        notification.send_notification(message)
    else:
        logging.info("All expected backups are present")
    logging.info("Backup check completed")