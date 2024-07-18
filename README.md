# Checkit

A flexible monitoring system for backup checks.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Automated Daily Checks (macOS)](#automated-daily-checks-macos)
- [Logs](#logs)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/hzheng/checkit.git
   cd checkit
   ```
2. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Usage

Run the Checkit command:

```
poetry run checkit
```

### Notes:

- By default, `APP_HOME` is set to `$HOME/.checkit`.
  - You can customize this with: `checkit -a my_checkit_home`
- Missing backup messages are sent to Todoist.
  - Set `TODOIST_API_KEY` in your environment, or
  - Pass it as an argument: `checkit -k my_todoist_api_key`

## Configuration

1. Copy the sample configuration file:
   ```
   cp config/backup_schedules.json.sample $APP_HOME/backup_schedules.json
   ```
2. Edit `$APP_HOME/backup_schedules.json` to set up your backup schedules.
   - Use Jenkins-style cron syntax for scheduling.

## Automated Daily Checks (macOS)

To set up automated daily checks:

1. Copy the run script:
   ```
   cp scripts/run_checkit.sh ~/scripts/run_checkit.sh
   chmod +x ~/scripts/run_checkit.sh
   ```

2. Copy and edit the launchd plist:
   ```
   cp scripts/checkit.plist.sample ~/Library/LaunchAgents/com.USERNAME.checkit.plist
   ```
   - Replace all instances of `/Users/USERNAME` with your home directory path
   - Replace `USERNAME` in the label with your macOS username
   - Replace `TODOIST_API_KEY` with your Todoist API key
   - Replace `DATA_BAK` with your root backup directory

3. Load the launch agent:
   ```
   launchctl load ~/Library/LaunchAgents/com.USERNAME.checkit.plist
   ```

This will run Checkit daily at 11 PM. To change the schedule, adjust the `StartCalendarInterval` in the plist file.

## Logs

Logs are stored in `$APP_HOME/logs/backup_check.log`.

---

For more detailed information or troubleshooting, please refer to the documentation or open an issue on the GitHub repository.
