import random
import logging
import threading
from datetime import datetime
from imgurpython import ImgurClient


class ImgurBot:
    def __init__(self, config, transport, username, check_interval):
        self.client = ImgurClient(config["client_id"], config["client_secret"])
        self.transport = transport
        self.username = username
        self.check_interval = check_interval
        self.last_notify_date = datetime.utcnow()

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.check_posts, daemon=True)
        self.thread.start()

    def wait(self):
        self.thread.join()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def get_latest_post(self):
        try:
            logging.debug("[ImgurBot] Checking latests posts from %s", self.username)
            posts = self.client.get_account_submissions(self.username, page=0)
            posts.sort(key=lambda x: x.datetime, reverse=True)
            return posts[0]
        except IndexError:
            return None
        except Exception as e:
            logging.warn("[ImgurBot] Failed to fetch latests posts: %s", e)

    def notify_post(self, post):
        message = "New post from {user}: {url}".format(
            user=self.username,
            url=post.link,
        )
        self.transport.send_message(message)

    def check_posts(self):
        while not self.stop_event.isSet():
            latest_post = self.get_latest_post()
            post_date = getattr(latest_post, "datetime", 0)
            post_date = datetime.fromtimestamp(post_date)

            logging.debug(
                "[ImgurBot] Latest post from %s is from %s, last notify was at %s",
                self.username,
                post_date,
                self.last_notify_date,
            )

            if latest_post and post_date > self.last_notify_date:
                self.notify_post(latest_post)
                self.last_notify_date = post_date

            # Wait a random amount of time before starting so not all requests
            # are sent at the same time
            wait_time = self.check_interval + random.randint(-30, 30)
            wait_time = max(wait_time, 0)
            self.stop_event.wait(wait_time)
