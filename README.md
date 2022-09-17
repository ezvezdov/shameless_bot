# Telegram bot for finding best jobs in shameless

Installation on arch linux:
```bash
sudo pacman -S python python-pip
sudo pip install pyTelegramBotAPI
```

# How it works
It parse web-site and reformate data with rules: \
a) cut off jobs what are 5+ hours \
b) cut off full capacity jobs \
c) cut off jobs with Založník role 

Programm will update data every minute. Bot send a message if something changes.

# How to use
Commands:
* /start - start bot and send job list 
* /help - get help message 
* /jobs - get actual jobs list
