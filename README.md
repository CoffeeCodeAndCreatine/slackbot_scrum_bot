# slackbot_scrum_bot
A simple python CLI that can be used to save and format scrum notes, and then post them directly to a slack channel.

## Main Features
1. Auto-formats text into a nice table so that it can be posted in a consistent format to a slack channel 
2. Slack bot integration allowing the python CLI to post scrum notes directly to a slack channel
3. Saves scrum notes history as both a text file and a json file. The text file can be used to review what you have done in plain text, while the json file will be used by the CLI to give you reminders on what you did the previous day. 

## Explanation of Files
1. history_json.json: A file used to store your past entries so that the CLI can give you reminders of what you worked on the previous day.
2. history_text.json: A file used to store your past entries in plain text for easy reading should you wish to see what you have worked on in the past.
3. slackbot_scrum_bot.py: Source code for the python CLI.
4. configs.json: Configuration file.  

## How to Configure the CLI
The CLI will walk you through the configuration on the first launch of the CLI. That being said, if you want to bypass this step, you can set up the configuration file yourself. To start, this is what the configuration file looks like. 
```json
{
  "slack_bot_token": "",
  "channel_token": "",
  "user_name": "",
  "number_prefix": "   ",
  "number_wrap": "50",
  "bullet_prefix": "    ",
  "bullet_wrap": "50"
}
```

1. slack_bot_token: This is going to be auth token for the bot user of the application that is set up in slack. If you are using this for a company, odds are they have a bot integration set up, if they don’t, or you are using this bot for personal use, you will have to set up your own app. If you are unsure on how to do this, take a look at the “How to Configure a Slack Bot” section below. 
2. channel_token: This is going to be the token of the slack channel you want the bot to post to. If you are unsure on how to get this token, take a look at the “How to Get a Slack Channel Token” section below.
3. user_name: This is the user name that the bot will call out when posting slack notes, I suggest just setting it to your first and last name. 
4. number_prefix: This is a prefix for numbered entries, I highly suggest leaving this as is, however if you want to customize it, you are welcome to do so.
5. number_wrap: This is how many characters will be printed before the table wraps, I suggest using 50, that way in slack you can split screen and still have things formatted nicely, but you are welcome to configure as you see fit.
6. bullet_prefix: This is a prefix for bullet entries, I highly suggest leaving this as is, however if you want to customize it, you are welcome to do so.
7. bullet_wrap: This is how many characters will be printed before the table wraps, I suggest using 50, that way in slack you can split screen and still have things formatted nicely, but you are welcome to configure as you see fit.


A bit 
## How to Run Python CLI
```bash
pip3 install -r requirements.txt
python3 scrum_bot.py
```

## How To Video
[Coming Soon]()
