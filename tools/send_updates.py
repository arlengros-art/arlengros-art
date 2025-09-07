#!/usr/bin/env python3
"""Send update emails to early adopters using Mailchimp API."""

import json
import os
from pathlib import Path

import requests

DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'early_adopters.json'

MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_SERVER_PREFIX = os.getenv('MAILCHIMP_SERVER_PREFIX')  # e.g., 'us5'
MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID')


def load_recipients() -> list[dict[str, str]]:
    with open(DATA_FILE, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def send_update(subject: str, content: str) -> None:
    if not (MAILCHIMP_API_KEY and MAILCHIMP_SERVER_PREFIX and MAILCHIMP_LIST_ID):
        raise RuntimeError('Mailchimp configuration missing in environment variables')

    url = f'https://{MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/messages'
    data = {
        'recipients': {'list_id': MAILCHIMP_LIST_ID},
        'subject_line': subject,
        'from_email': 'no-reply@example.com',
        'from_name': 'Project Updates',
        'to': load_recipients(),
        'html': content,
    }
    response = requests.post(url, auth=('anystring', MAILCHIMP_API_KEY), json=data)
    response.raise_for_status()
    print('Mailchimp response:', response.json())


if __name__ == '__main__':
    send_update('Project Update', '<p>Спасибо за то, что вы с нами!</p>')
