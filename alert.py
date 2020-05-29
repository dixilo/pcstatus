#!/usr/bin/env python3
'''Alert using Slack
'''
from slacker import Slacker
from pathlib import Path

import yaml

PATH_SETTING = Path(__file__).parent.joinpath('alert_setting.yaml')

def send_alert(message, hostname):
    with open(PATH_SETTING) as f:
        setting = yaml.safe_load(f)

    api_token = setting['slack_setting']['api_token']
    channel = setting['slack_setting']['channel']
    slackbot = Slacker(api_token)

    slackbot.chat.post_message(channel, f'[{hostname}]\n{message}', as_user=True)


def main():
    '''Test code
    '''
    send_alert('test', 'test')


if __name__ == '__main__':
    main()
