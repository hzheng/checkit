import logging

from todoist_api_python.api import TodoistAPI

from checkit.utils import config

def create_todoist_task(content):
    api = TodoistAPI(config.TODOIST_API_KEY)
    try:
        task = api.add_task(content=content, due_string="today")
        logging.info(f"Todoist task created: {task.content}")
    except Exception as error:
        logging.error(f"Error creating Todoist task: {error}")

def send_notification(message):
    create_todoist_task(message)
