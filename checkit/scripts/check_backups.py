import os
import logging

from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from croniter import croniter

from checkit.utils import config, notification

def setup_logging():
    log_file = config.get_log_file()
    max_log_size = 100 * 1024 * 1024  # 100 MB
    backup_count = 10  # Number of backup files to keep
    handler = RotatingFileHandler(
        log_file,
        maxBytes=max_log_size,
        backupCount=backup_count
    )
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def get_prev_backup_time(schedule, now):
    cron = croniter(schedule, now)
    return cron.get_prev(datetime)

def check_backups():
    now = datetime.now()
    grace_period_minutes = config.GRACE_PERIOD_MINUTES
    grace_period = timedelta(minutes=grace_period_minutes)
    missing_backups = []
    for subdir, schedule in config.BACKUP_SCHEDULES.items():
        prev_backup_time = get_prev_backup_time(schedule, now)
        check_time = prev_backup_time - grace_period
        dir_path = os.path.join(config.BACKUP_DIR, subdir)
        if not os.path.exists(dir_path):
            logging.warning(f"Directory {dir_path} does not exist.")
            missing_backups.append(subdir)
            continue

        backup_found = False
        logging.info(f"Checking backup for '{subdir}'. Expected: {prev_backup_time.isoformat()}, Checking since: {check_time.isoformat()}")
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime > check_time:
                    logging.info(f"Backup found for {subdir}: {file}")
                    backup_found = True
                    break
        
        if not backup_found:
            missing_backups.append(subdir)
            logging.warning(f"Backup missing for {subdir}.")

    return missing_backups, now

def run():
    setup_logging()
    logging.info("Starting backup check")
    missing_backups, check_time = check_backups()
    if missing_backups:
        message = f"Detected missing backups: {', '.join(missing_backups)} on {check_time.isoformat(timespec='seconds')}"
        logging.warning(message)
        notification.send_notification(message)
    else:
        logging.info("All expected backups are present")
    logging.info("Backup check completed")