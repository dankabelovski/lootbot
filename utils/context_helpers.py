# utils/context_helpers.py

from telegram import Update

def get_effective_message(update: Update):
    return update.message or (update.callback_query and update.callback_query.message)
