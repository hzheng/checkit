import argparse
import os

from checkit.scripts import check_backups
from checkit.utils import config

def parse_arguments():
    parser = argparse.ArgumentParser(description="Checkit: A flexible monitoring system")
    parser.add_argument("-k", "--api-key", help="Todoist API key")
    parser.add_argument("-d", "--backup-dir", help="Backup directory path")
    parser.add_argument("-a", "--app-home", 
                        default=os.path.expanduser('~/.checkit'),
                        help="Application home directory (default: ~/.checkit)")
    parser.add_argument("-s", "--schedule-file", 
                        help="JSON file containing backup schedules (default: APP_HOME/backup_schedules.json)")
    parser.add_argument("-g", "--grace-period", 
                        type=int, 
                        default=30, 
                        help="Grace period in minutes (default: 30)")
    parser.add_argument("-m", "--max-backup-days", 
                        type=int, 
                        default=1, 
                        help="Maximum age of backups in days (default: 1)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    config.load_config(args)
    check_backups.run()

if __name__ == "__main__":
    main()