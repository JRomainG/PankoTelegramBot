#!/usr/bin/env python3
import logging
import argparse
import configparser

from backend import ImgurBot
from transport import TelegramTransport


def main():
    # Load the Imgur and Telegram auth info
    auth_config = configparser.ConfigParser()
    auth_config.read("auth.ini")

    # Create a bot for each user
    bots = []

    config = configparser.ConfigParser()
    config.read("config.ini")

    for user in config.sections():
        # Create a "transport" to send Telegram messages
        chat_id = config[user]["chat_id"]
        transport = TelegramTransport(auth_config["Telegram"], chat_id)

        # Create an Imgur bot using this transport
        logging.info("Creating bot for user %s...", user)
        username = config[user]["username"]
        interval = config[user].getint("check_interval", 3600)
        bot = ImgurBot(auth_config["Imgur"], transport, username, interval)
        bots.append(bot)

    # Wait for all bots and make sure to stop them all once we're done
    logging.info("Started %d bot(s)", len(bots))
    try:
        print("Use Ctrl+C to stop")
        for bot in bots:
            bot.wait()
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Stopping all bots...")
        for bot in bots:
            bot.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PankoBot")
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    args = parser.parse_args()

    level = args.log_level.upper()
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )
    main()
