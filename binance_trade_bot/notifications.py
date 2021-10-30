import queue
import threading
import telebot
from os import path

import apprise

APPRISE_CONFIG_PATH = "config/apprise.yml"

class NotificationHandler:
    def __init__(self, enabled=True):
        self.bot = telebot.TeleBot("2069364847:AAH7dgTfohJ3gckW6i4RA5Fd80_w-5zWFSg", parse_mode=None)
        if enabled and path.exists(APPRISE_CONFIG_PATH):
            self.apobj = apprise.Apprise()
            config = apprise.AppriseConfig()
            config.add(APPRISE_CONFIG_PATH)
            self.apobj.add(config)
            self.queue = queue.Queue()
            self.start_worker()
            self.enabled = True
        else:
            self.enabled = False

    def start_worker(self):
        threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        while True:
            message, attachments = self.queue.get()

            if attachments:
                self.apobj.notify(body=message, attach=attachments)
            else:
                self.apobj.notify(body=message)
            self.queue.task_done()

    def send_notification(self, message, attachments=None):
        if self.enabled:
            self.queue.put((message, attachments or []))

    def send_telegram_notification(self, message):
        try:
            self.bot.send_message(360270449, message)
        except Exception as error:
            # self.bot.send_message(360270449, "[Error] "+ error)
            print("Error:", error)
            print("Message:", message)