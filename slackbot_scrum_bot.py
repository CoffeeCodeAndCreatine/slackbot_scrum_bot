import json
import os
import sys
import textwrap
from datetime import date, timedelta, datetime

from colorama import init
from pyfiglet import figlet_format
from slackclient import SlackClient
from termcolor import cprint
from terminaltables import AsciiTable

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


def check_config():
    tokens = {}

    with open('configs.json') as json_data:
        tokens = json.load(json_data)

    if tokens["slack_bot_token"] == "" or tokens["channel_token"] == "" or tokens["user_name"] == "":
        cprint(figlet_format('SHIT!'), 'red', attrs=['bold'])
        cprint(
            "It looks like someone forgot to set up my config file...\nLet's walk though it together, this will be easy.",
            'red')

        user_name = input("What is your name? Please give me your First and Last name."
                          "\n\t>>")
        cprint("\nThank you " + user_name + ". That's a lovely name.", 'red')

        slack_bot_token = input(
            "What is your bot's slack bot token? This will be the token bound to the bot configured in the slack page. It will look something like this: xoxb-1234567890-123456789012-qyfhgjbmkdpeomnsjditnasm."
            "\n\t>>")
        cprint("\nSweet! nice token.", 'red')

        channel_token = input(
            "What is the channel token? This will be the id for the specific channel you post notes to. It should look something like this: A0ABCDE0A."
            "\n\t>>")
        cprint("\nCool! I have heard good things about that channel.", 'red')

        number_wrap = input("How many characters would you like to display before I wrap numbered text?"
                            "\nI suggest 50."
                            "\n\t>>")
        cprint("\nGreat!", 'red')

        number_prefix = input("What would you like your number prefix to be?"
                              "\nI suggest 3 spaces, '   '."
                              "\n\t>>")
        cprint("\nLovely!", 'red')

        bullet_wrap = input("How many character would you like to display before I wrap bulleted text?"
                            "\nI suggest 50."
                            "\n\t>>")
        cprint("\nWonderful!", 'red')

        bullet_prefix = input("What would you like your bullet prefix to be?"
                              "\nI suggest 4 spaces, '    '."
                              "\n\t>>")
        cprint("\nRight on!", 'red')

        cprint(
            "\nNow that we have that set up, I am going to go ahead and save those values so we don't have to do this again\n\tpress enter to continue",
            'green')
        enter = input("")

        tokens['slack_bot_token'] = slack_bot_token
        tokens['channel_token'] = channel_token
        tokens['user_name'] = user_name
        tokens['number_wrap'] = number_wrap
        tokens['bullet_wrap'] = bullet_wrap
        tokens['number_prefix'] = number_prefix
        tokens['bullet_prefix'] = bullet_prefix

        with open('configs.json', 'w') as outfile:
            json.dump(tokens, outfile)

    os.system('cls' if os.name == 'nt' else 'clear')
    return tokens


def get_previous_work_day():
    day = datetime.today().weekday()
    if day == 0:
        # it's monday, pull friday date
        return (date.today() - timedelta(2)).strftime("%m/%d/%Y")
    return (date.today() - timedelta(1)).strftime("%m/%d/%Y")


def get_previous_day_work(previous_date):
    history = {}
    with open('history_json.json') as json_data:
        history = json.load(json_data)

    history = history.get(previous_date)
    if history == None:
        print("\nI was unable to load previous work. I am sorry.")

    return history


def print_title():
    cprint(figlet_format('Scrum Bot', font='chunky'), 'blue', attrs=['bold'])


def print_instructions():
    print("Welcome to Scrum Bot!!"
          "\nI am here to help you format and post your scrum notes to your scrum channel."
          "\nFirst I will ask you to tell me about what you did yesterday."
          "\nSecond I will ask you about what you plan to do today."
          "\nThird I will ask you about your blockers."
          "\nFourth I will ask you about and notes."
          "\n"
          "\nJust so you know, if you want a nested bullet, you may prepend '--' to any line."
          "\nFor example"
          "\n\tThis was a task I did"
          "\n\t--This was a sub task for that task")


def print_previous_day_prompt():
    print("\nPlease enter any tasks that you worked on yesterday.")


def print_previous_day_reminder(previous_day_work):
    if previous_day_work != None and bool(previous_day_work):
        print("\n\nAs a reminder, this is what you were working on.\n")

        for work_item in previous_day_work['today']:
            row_string = work_item['task']

            sub_tasks = work_item['sub_tasks']
            for sub_task in sub_tasks:
                row_string = row_string + "\n  > " + sub_task

            cprint(str(row_string), 'yellow')


def print_today_prompt():
    print("\nPlease enter any tasks that you intend to work on today.")


def print_blockers_prompt():
    print("\nPlease enter any blockers you currently have.")


def print_notes_prompt():
    print("\nPlease enter any notes you would like to share.")


def get_task_list(number_prefix, bullet_prefix, number_wrap, bullet_wrap):
    wrapper = []
    index = 0
    while True:
        input_item = input("\t>>")
        if input_item == "":
            break
        elif input_item[:2] == "--":
            input_item = str(textwrap.indent(textwrap.fill(input_item, bullet_wrap), bullet_prefix))[6:]

            task = wrapper[(len(wrapper)) - 1]
            del wrapper[-1]

            sub_tasks = task['sub_tasks']
            sub_tasks.append(input_item)

            task['sub_tasks'] = sub_tasks
            wrapper.append(task)
        else:
            input_item = str(textwrap.indent(textwrap.fill(input_item, number_wrap), number_prefix))[3:]
            main_task = {}
            main_task['task'] = str(index) + ": " + input_item
            main_task['sub_tasks'] = []
            wrapper.append(main_task)
            index += 1
    return wrapper


def generate_table_string(table_json, user_name, date):
    table_string = [[user_name + "\n" + str(date), '']]

    table_string.append(['Previous', ''])
    for previous in table_json['previous_day']:
        row_string = previous['task']

        sub_tasks = previous['sub_tasks']
        for sub_task in sub_tasks:
            row_string = row_string + "\n  > " + sub_task

        tmp = ['', row_string]
        table_string.append(tmp)

    table_string.append(['Today', ''])
    for today in table_json['today']:
        row_string = today['task']

        sub_tasks = today['sub_tasks']
        for sub_task in sub_tasks:
            row_string = row_string + "\n  > " + sub_task

        tmp = ['', row_string]
        table_string.append(tmp)

    table_string.append(['Blockers', ''])
    for today in table_json['blockers']:
        row_string = today['task']

        sub_tasks = today['sub_tasks']
        for sub_task in sub_tasks:
            row_string = row_string + "\n  > " + sub_task

        tmp = ['', row_string]
        table_string.append(tmp)

    table_string.append(['Notes', ''])
    for today in table_json['notes']:
        row_string = today['task']

        sub_tasks = today['sub_tasks']
        for sub_task in sub_tasks:
            row_string = row_string + "\n  > " + sub_task

        tmp = ['', row_string]
        table_string.append(tmp)

    return AsciiTable(table_string)


def print_table_string(table_string):
    print("\nI have generated the following table based on your input")
    print(table_string.table)


def save_history_text(table_string):
    with open("history_text.txt", "a") as history_text:
        history_text.write(table_string.table + "\n\n")


def send_to_slack(table_string, user_name, slack_bot_token, slack_channel_token):
    cprint("\n\nWould you like me to send these notes to slack?\n\tYes = 1\n\tNo = 0", 'green')
    send_update = input("\t>>")
    if send_update == "1":
        message = "POSTING SCRUM NOTES FOR `" + user_name + "`\n```" + table_string.table + "```"
        send_slack_message(message, slack_channel_token, slack_bot_token)
        cprint("\nScrum notes sent!", 'green')
    else:
        cprint("\nScrum notes NOT sent", 'red')


def send_slack_message(msg, channel, slack_bot_token):
    slack_client = SlackClient(slack_bot_token)
    response = slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=msg,
        as_user=True
    )
    handle_bad_response(response)


def handle_bad_response(response):
    if not response['ok']:
        print("Slack API error: " + response['error'])
        return None
    return response


def save_history_json(table_json, date):
    history = {}
    with open('history_json.json') as in_file:
        history = json.load(in_file)

    history[date] = table_json

    with open('history_json.json', 'w') as outfile:
        json.dump(history, outfile)


def print_exit():
    cprint(figlet_format('Exited', font='chunky'), 'blue', attrs=['bold'])


def main():
    tokens = check_config()

    today_date = date.today().strftime("%m/%d/%Y")
    previous_date = get_previous_work_day()


    print_title()
    print_instructions()
    task_container = {}

    previous_day_work = get_previous_day_work(previous_date)

    print_previous_day_reminder(previous_day_work)
    print_previous_day_prompt()
    task_container['previous_day'] = get_task_list(tokens['number_prefix'], tokens['bullet_prefix'],
                                                   int(tokens['number_wrap']), int(tokens['bullet_wrap']))

    print_today_prompt()
    task_container['today'] = get_task_list(tokens['number_prefix'], tokens['bullet_prefix'],
                                            int(tokens['number_wrap']), int(tokens['bullet_wrap']))

    print_blockers_prompt()
    task_container['blockers'] = get_task_list(tokens['number_prefix'], tokens['bullet_prefix'],
                                               int(tokens['number_wrap']), int(tokens['bullet_wrap']))

    print_notes_prompt()
    task_container['notes'] = get_task_list(tokens['number_prefix'], tokens['bullet_prefix'],
                                            int(tokens['number_wrap']), int(tokens['bullet_wrap']))

    table_string = generate_table_string(task_container, tokens['user_name'], today_date)
    print_table_string(table_string)

    save_history_text(table_string)
    save_history_json(task_container, today_date)

    send_to_slack(table_string, tokens['user_name'], tokens["slack_bot_token"], tokens['channel_token'])

    print_exit()


if __name__ == "__main__":
    main()
