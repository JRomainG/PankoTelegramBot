# PankoBot

A Telegram bot to automatically notify when specific users upload new posts to
Imgur using the [Imgur API](https://apidocs.imgur.com).

## Installation

PankoBot requires Python 3.7 or newer.

Dependencies can be installed using pip:

```bash
$ pip3 install -r requirements.txt
```

## Configuration

You need to create two files: `auth.ini` and `config.ini`:

```bash
$ cp auth.ini.example auth.ini
$ cp config.ini.example config.ini
```

### Imgur

You must register your client with the Imgur API, as detailed in the [official
documentation](https://api.imgur.com/#registerapp):

1. Visit [this url](https://api.imgur.com/oauth2/addclient) to register a new
   client,
2. Enter an `Application name`,
3. Select `Anonymous usage without user authorization` under `Authorization
   type`,
4. Enter any `Authorization callback URL` (e.g. `https://imgur.com`),
5. Enter an `Email` and `Description`, solve the captcha, and click `submit`.

Imgur should then provide you with a `client_id` and `client_secret`, which you
should save in the `auth.ini` file for the bot to use.

### Telegram

To send messages using Telegram, you first need to create a [Telegram
bot](https://core.telegram.org/bots). For this, you need to talk to
[BotFather](https://t.me/botfather) and issue the `/newbot` command. Once you
are done, BotFather will provide you with a token, save it in the `auth.ini`
file.

Once this is done, you can invite your bot to a Telegram group or channel and
retrieve its chat id. After inviting the bot, you can find the chat ID from the
`https://api.telegram.org/bot{token}/getUpdates` URL (replacing `{token}` with
your bot's token).

### PankoBot

Finally, you can configure this script by editing the `config.ini` file. Here
are the available options:

| Key                  | Type   | Description                                                          |
| -------------------- | ------ | -------------------------------------------------------------------- |
| username             | string | The username of the Imgur user you want to follow  (e.g. PankoBoy)   |
| check_interval       | int    | How often to check for new posts (in seconds, default is 3600)       |
| chat_id              | string | The ID of the Telegram chat to which messages are sent               |
| silent_notifications | bool   | Whether to send messages silently (notifications will have no sound) |

## Running

Simply start the script and let it run in the background:

```bash
$ python3 main.py
```

### Docker

You can run the bot directly using [Docker](https://www.docker.com):

```bash
$ docker build . -t pankobot
$ docker run -d pankobot
```

### Systemd service

If you use systemd, you can run the bot as a service. Here is an example
configuration file:

```
[Unit]
Description=PankoBot
After=network.target

[Service]
User=bot
Nice=1
KillMode=mixed
SuccessExitStatus=0 1
ProtectHome=true
ProtectSystem=full
PrivateDevices=true
NoNewPrivileges=true
WorkingDirectory=/var/bots/
ExecStart=/usr/bin/python3 /var/bots/PankoBot/main.py
#ExecStop=

[Install]
WantedBy=multi-user.target
```

You can save it as `/etc/systemd/system/PankoBot.service`, and then start it:

```bash
$ systemctl daemon-reload
$ systemctl enable PankoBot
$ systemctl start PankoBot
```
