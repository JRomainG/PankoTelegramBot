import logging
from telegram import Bot


class TelegramTransport:
    def __init__(self, config, chat_id, silent):
        self.tg_bot = Bot(token=config["token"])
        self.chat_id = chat_id
        self.silent = silent

    def send_message(self, text):
        logging.debug("[TelegramTransport] Sending message:\n%s", text)
        self.tg_bot.send_message(
            chat_id=self.chat_id, text=text, disable_notification=self.silent
        )
