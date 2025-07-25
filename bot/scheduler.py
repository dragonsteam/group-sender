from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telethon.sync import functions
from telethon.types import DialogFilterDefault, InputPeerEmpty

from .base import fix_event_loop, get_client
from .db import get_user_phone, get_api_connected, unauthorize
from .auth import start_auth

import logging


# Global Scheduler Instance
scheduler = BackgroundScheduler()
scheduler.start()

# Dictionary to store user-specific tasks
user_tasks = {}


def get_dialog_filter(client, filter_id):
    dialog_filters = client(functions.messages.GetDialogFiltersRequest())
    
    for dialog_filter in dialog_filters.filters:
        if type(dialog_filter) == DialogFilterDefault:
            continue
        
        if dialog_filter.id == filter_id:
            return dialog_filter
        

def my_task(user_id, folder_id, text):
    try:
        fix_event_loop()

        user_phone = get_user_phone(user_id)
        api = get_api_connected(user_id)

        with get_client(user_phone, api.api_id, api.api_hash) as client:
            # # Get only dialogs in the specific folder
            # result = client(functions.messages.GetDialogsRequest(
            #     offset_date=None,
            #     offset_id=0,
            #     offset_peer=InputPeerEmpty(),
            #     limit=100,  # Adjust limit as needed
            #     hash=0,
            #     folder_id=folder_id  # Fetch only dialogs from this folder
            # ))

            dialog_filter = get_dialog_filter(client, folder_id)
            for peer in dialog_filter.include_peers:
                entity = client.get_entity(peer)
                client.send_message(entity, text)
                # message = client.get_messages('yevauzbot', ids=message_id)

            # for dialog in result.dialogs:
            #     entity = client.get_entity(dialog.peer)  # Resolve entity
            #     client.send_message(entity, MESSAGE)
            #     print(f"Sent message to: {entity.title if hasattr(entity, 'title') else entity.username}")
  

            # dialog_filters = client(functions.messages.GetDialogFiltersRequest())
        
            # for dialog_filter in dialog_filters.filters:
            #     if type(dialog_filter) == DialogFilterDefault:
            #         continue

            #     if dialog_filter.id == folder_id:
            #         logging.warning(dialog_filter)
            #         client.send_message(folder_id, "🦀")
    except Exception as e:
        if type(e) == EOFError:
            unauthorize(user_id)
            start_auth(chat_id=user_id)
            return
        
        logging.error(f">>> Error on executing task for user: {user_id}")
        logging.error(e)
        stop_task(user_id=user_id)
    

def create_task(user_id, folder_id, text, interval = 3):
    """Start a new periodic task for the user"""
    job_id = f"user_task_{user_id}"

    if job_id in user_tasks:
        stop_task(user_id)
    
    job = scheduler.add_job(
        my_task,
        trigger=IntervalTrigger(minutes=interval),
        id=job_id,
        args=[user_id, folder_id, text],
        next_run_time=datetime.now(),
    )
    user_tasks[job_id] = job
    # logging.warning(f"Task started for User {user_id}!")

def stop_task(user_id):
    """Stop the periodic task for the user"""
    job_id = f"user_task_{user_id}"
    
    if job_id in user_tasks:
        scheduler.remove_job(job_id)
        del user_tasks[job_id]
        # logging.warning(f"Task stopped for User {user_id}!")
