# Telegram bot for finding best jobs in [shameless](shameless.sinch.cz)

Installation on arch linux:
```bash
sudo pacman -S python python-pip
pip install pyTelegramBotAPI
```

# How it works
It parse web-site and reformate data with rules: \
a) cut off jobs what are 5+ hours \
b) cut off full capacity jobs \
c) cut off jobs with Založník role \
d) cut off joined jobs if one of joined jobs does not comply with the rules from above

Programm will update data every minute. Bot send a message if something changes.

# How to use
Commands:
* /start - start bot and send job list 
* /stop - stop refreshing (bot is working)
* /continue - continue refreshing data
* /help - get help message 
* /info - info about current bot condition
* /jobs - get actual jobs list
