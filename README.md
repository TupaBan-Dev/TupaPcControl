<div align="center">
  <h1>TupaPcConrol - Bot</h1>
  <h3>A bot for remote computer management using telegram</h3>
</div><br>

## Launch
1) To get started, copy this repository
2) Then download all the necessary libraries with this command -
```sh
pip install -r requirements.txt
```
3) Change bot_token, admin_id, and bot_password in config.ini
4) Run the bot with this command -
```sh
python main.py
```
5) Send the command to the bot /password example - where the example is the bot_password that you specified in the config

## Configuring
1) bot_token - The bot token that you can get from @BotFather
2) bot_password - The password from the bot, which you can come up with yourself, is used to call the inline menu
3) admin_id - Your ID
4) start_message - Whether to respond to the /start command (off, on)
5) startup_message - Should I write a message to the administrator about the launch of the bot (off, on)
6) shutdown_message - Should I write a message to the administrator about turning off the bot (off, on)